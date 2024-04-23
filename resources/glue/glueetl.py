from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import concat_ws, split, explode, col
from pyspark.sql import SparkSession
import os
import sys
import boto3 


args = getResolvedOptions(sys.argv, ['S3BucketData', 'S3AdminData', 'AdminCatalog', 
                                     'AdminUsersTable', 'AdminUserFollowers', 'AdminTweets', "TempDir"])

DATABASE = args['AdminCatalog']
S3_BUCKET = args['S3AdminData']
TARA_ACADEMY_FINAL_DATABASE = args['S3BucketData']
TABLE_USERS=args['AdminUsersTable']
TABLE_FOLLOWERS=args['AdminUserFollowers']
TABLE_TWEETS=args['AdminTweets']

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
bucket_contents = s3_client.list_objects(Bucket=S3_BUCKET)
spark_context = SparkContext()
spark = SparkSession(spark_context)
glue_context = GlueContext(spark_context)
job = Job(glue_context)

def get_partitions_num_from_redshift():
    """
    Retrieves the number of partitions for specific Redshift tables related to Twitter data.

    This function connects to a Redshift database and fetches information about the number of partitions
    for tables storing Twitter data, including 'public.read_tara_users', 'public.read_tara_tweets', and
    'public.read_tara_followers'.

    Returns:
        tuple: A tuple containing the number of partitions for each table in the following order:
            - Number of partitions for 'public.read_tara_tweets'
            - Number of partitions for 'public.read_tara_users'
            - Number of partitions for 'public.read_tara_followers'
    """
    
    redshift_table_names = ["public.read_tara_users", "public.read_tara_tweets", "public.read_tara_followers"]
    for table in redshift_table_names:
        connection_options = {
            "url": "jdbc:redshift://admin-academy-redshift.c76boardkpkb.eu-central-1.redshift.amazonaws.com:5439/twitter_redshift_db",
            "dbtable":table,
            "user": "admin",
            "password": "Academy2023!",
            "redshiftTmpDir": args["TempDir"]
        }
        df = glue_context.create_dynamic_frame_from_options("redshift", connection_options).toDF()
        glue_df = df.select("num_partitions", "table_folder")
        if table == "public.read_tara_users":
            users_df = glue_df.filter(glue_df["table_folder"] == "users")
            users_value = users_df.first()["num_partitions"]
        if table == "public.read_tara_tweets":
            tweets_df = glue_df.filter(glue_df["table_folder"] == "tweets")
            tweets_value = tweets_df.first()["num_partitions"]
        if table == "public.read_tara_followers":
            followers_df = glue_df.filter(glue_df["table_folder"] == "followers")
            followers_value = followers_df.first()["num_partitions"]
            
    return tweets_value, users_value, followers_value

def get_partitions_from_S3(s3_bucket_content: dict) -> tuple:
    """
    Retrieves S3 partition keys for Twitter data stored in an S3 bucket.

    This function scans the contents of an S3 bucket and identifies partition keys for Twitter data
    related to users, user followers, and tweets. It categorizes the partition keys into separate lists
    based on their prefixes, such as 'users', 'user_followers', and 'tweets'.

    Returns:
        tuple: A tuple containing lists of partition keys for different Twitter data categories in the following order:
            - List of partition keys for 'tweets'
            - List of partition keys for 'users'
            - List of partition keys for 'user_followers'
    """
    
    partition_users = []
    partition_followers = []
    partition_tweets = []
    for obj in s3_bucket_content.get('Contents', []):
        key = obj['Key']
        parts = key.split('/')
        for part in parts:
            if part.startswith("users"):
                partition_users.append(key)
            elif part.startswith("user_followers"):
                partition_followers.append(key)
            elif part.startswith("tweets"):
                partition_tweets.append(key)
                
    return partition_tweets, partition_users, partition_followers
    
def write_data_to_redshift(length: int, table_name: str, col_data: str) -> None:
    """
    Writes data to an Amazon Redshift database table using Apache Spark.

    Parameters:
    - length (int): The length of the data to be inserted into the Redshift table.
    - table_name (str): The name of the target Redshift table where data will be written.
    - col_data (str): The data to be inserted into the 'table_folder' column.

    This function takes the specified data, length, and table name, and uses Apache Spark to create a DataFrame
    containing the data. It then writes this DataFrame to the specified Amazon Redshift table, overwriting any
    existing data in the table.

    """
    
    redshift_options = {
    "url": "jdbc:redshift://admin-academy-redshift.c76boardkpkb.eu-central-1.redshift.amazonaws.com:5439/twitter_redshift_db",
    "driver": "com.amazon.redshift.jdbc42.Driver",
    "user": "admin",
    "password": "Academy2023!"
    }
    data = [(1, col_data, length)]
    columns = ["id", "table_folder", "num_partitions"]
    df = spark.createDataFrame(data, columns)
    df.write.jdbc(url=redshift_options["url"], table=table_name, mode="overwrite", properties=redshift_options)
    
def create_DynamicFrame(partition: str) -> DynamicFrame:
    """
    Create a Glue DynamicFrame from data stored in an Amazon S3 bucket.

    Parameters:
    - partition (str): The partition or subdirectory within the S3 bucket where the data is located.

    Returns:
    - DynamicFrame: A Glue DynamicFrame containing the data from the specified S3 partition.
    """
    
    table = glue_context.create_dynamic_frame_from_options(
        connection_type="s3",
        connection_options={
            "paths": [f"s3://admin-academy-data/{partition}"]
        },
        format="parquet"
        ).repartition(1)
        
    return table
   
def write_DynamicFrame_to_s3(table: DynamicFrame, database: str, table_name: str) -> None:
    """
    Write a Glue DynamicFrame to an Amazon S3 bucket in Glue Parquet format.

    Parameters:
    - table (DynamicFrame): The Glue DynamicFrame containing the data to be written.
    - database (str): The name of the Glue database associated with the table.
    - table_name (str): The name of the table within the Glue database.

    This function takes a Glue DynamicFrame, converts it to a Spark DataFrame for compatibility, and then
    writes it to an Amazon S3 bucket in the Glue Parquet format. The S3 location where the data is written
    is specified by the 'database' and 'table_name' parameters.
    """
    
    table = table.toDF()
    table = DynamicFrame.fromDF(table, glue_context, "convert")
    glue_context.write_dynamic_frame.from_options(
            frame=table,
            connection_type="s3",
            format="glueparquet",
            connection_options={
                "path": f"s3://{database}/datalake/{table_name}"
            },
            format_options={"compression": "snappy"},
            transformation_ctx=f"output_data_{table_name}"
        )
        
def get_data_users(data_catalog: str, table_name: str, s3_bucket: str, partitions: list, index: int) -> None:
    """
    Retrieve, transform, and write users data to an S3 bucket using Glue DynamicFrames.

    Parameters:
    - data_catalog (str): The Glue Data Catalog database name containing the source table.
    - table_name (str): The name of the source table within the Glue Data Catalog.
    - s3_bucket (str): The S3 bucket where the transformed data will be written.
    - partitions (list): A list of partition names or subdirectories within the S3 bucket.
    - index (int): The starting index in the 'partitions' list to begin processing.

    This function retrieves users data stored in specified S3 partitions, transforms it by splitting
    users into separate records, and writes the transformed data to a new S3 location in Glue Parquet format.
    """
    
    for partition in partitions[index:]:
        
        # Create a DynamicFrame from the S3 table
        table = create_DynamicFrame(partition)
        
        table = DropFields.apply(frame = table, paths = ['user_id_str', 'profile_location', 'derived', 'url', 'verified', 
                                      'listed_count', 'favourites_count', 'created_at', 'default_profile',
                                     'withheld_in_countries', 'withheld_scope'])
                                     
        write_DynamicFrame_to_s3(table, s3_bucket, table_name)

    write_data_to_redshift(len(partitions), table_name="public.read_tara_users", col_data="users")

def get_data_followers(data_catalog: str, table_name: str, s3_bucket: str, partitions: list, index: int) -> None:
    """
    Retrieve, transform, and write follower data to an S3 bucket using Glue DynamicFrames.

    Parameters:
    - data_catalog (str): The Glue Data Catalog database name containing the source table.
    - table_name (str): The name of the source table within the Glue Data Catalog.
    - s3_bucket (str): The S3 bucket where the transformed data will be written.
    - partitions (list): A list of partition names or subdirectories within the S3 bucket.
    - index (int): The starting index in the 'partitions' list to begin processing.

    This function retrieves follower data stored in specified S3 partitions, transforms it by splitting
    followers into separate records, and writes the transformed data to a new S3 location in Glue Parquet format.
    """
    
    for partition in partitions[index:]:
        # Create a DynamicFrame from the S3 table
        table = create_DynamicFrame(partition)
        table = table.toDF()
        table = table.withColumn("followers_string", concat_ws(",", "followers"))
        table = table.withColumn("followers_array", split(table["followers_string"], ","))
        table = table.withColumn("follower", explode(table["followers_array"]))
        table = table.drop("followers", "followers_array", "followers_string")
        table = DynamicFrame.fromDF(table, glue_context, "convert")
        
        glue_context.write_dynamic_frame.from_options(
            frame=table,
            connection_type="s3",
            format="glueparquet",
            connection_options={
                "path": f"s3://{s3_bucket}/datalake/{table_name}"
            },
            format_options={"compression": "snappy"},
            transformation_ctx=f"output_data_{table_name}"
        )

    write_data_to_redshift(len(partitions), table_name="public.read_tara_followers", col_data="followers")
    
def get_data_tweets(data_catalog: str, table_name: str, s3_bucket: str, partitions: list, index: int) -> None:
    """
    Retrieve, transform, and write tweets data to an S3 bucket using Glue DynamicFrames.

    Parameters:
    - data_catalog (str): The Glue Data Catalog database name containing the source table.
    - table_name (str): The name of the source table within the Glue Data Catalog.
    - s3_bucket (str): The S3 bucket where the transformed data will be written.
    - partitions (list): A list of partition names or subdirectories within the S3 bucket.
    - index (int): The starting index in the 'partitions' list to begin processing.

    This function retrieves tweets data stored in specified S3 partitions, transforms it by splitting
    tweets into separate records, and writes the transformed data to a new S3 location in Glue Parquet format.
    """
    
    for partition in partitions[index:]:
        table = create_DynamicFrame(partition)
        table = DropFields.apply(frame = table, paths = ['user_id_str', 'possibly_sensitive', 'in_retweet_timedelta_sec', 'retweet_timedelta_sec', 'in_quote_timedelta_sec', 'tweets_dt'])
        table = table.toDF()
        table = DynamicFrame.fromDF(table, glue_context, "convert")
        write_DynamicFrame_to_s3(table, s3_bucket, table_name)

    write_data_to_redshift(len(partitions), table_name="public.read_tara_tweets", col_data="tweets")
 
tweets_value, users_value, user_followers_value = get_partitions_num_from_redshift()
partition_tweets, partition_users, partition_followers = get_partitions_from_S3(bucket_contents)

if user_followers_value != len(partition_followers):
    get_data_followers(DATABASE, TABLE_FOLLOWERS, TARA_ACADEMY_FINAL_DATABASE, partition_followers, user_followers_value)

if tweets_value != len(partition_users):
    get_data_tweets(DATABASE, TABLE_TWEETS, TARA_ACADEMY_FINAL_DATABASE, partition_tweets, tweets_value)

if users_value != len(partition_users):
    get_data_users(DATABASE, TABLE_USERS, TARA_ACADEMY_FINAL_DATABASE, partition_users, users_value)
    
job.commit()

