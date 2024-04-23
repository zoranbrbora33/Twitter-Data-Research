# AWS Glue ETL Pipeline Documentation
Overview
This documentation describes an ETL (Extract, Transform, Load) pipeline implemented in Python using the AWS Glue service and Apache Spark. The primary purpose of this ETL pipeline is to extract data from various sources, transform it into a suitable format, and load it into Amazon Redshift and Amazon S3. The pipeline focuses on processing Twitter data related to users, user followers, and tweets.

## Prerequisites
Before running this ETL pipeline, ensure that the following prerequisites are met:

Dependencies: Install the required Python libraries and dependencies, including pyspark, boto3, and AWS Glue libraries (awsglue, awsglue.transforms, awsglue.utils, awsglue.job, awsglue.dynamicframe).

## Code Structure
The ETL pipeline consists of several components:

### Environment variables
DATABASE = "admin-academy-twitter" <br>
S3_BUCKET = "admin-academy-data" <br>
TARA_ACADEMY_FINAL_DATABASE = "tara-academy-data" <br>
TABLE_USERS = "users" <br>
TABLE_FOLLOWERS = "user_followers" <br>
TABLE_TWEETS = "tweets"

### Initialization and Configuration: 
The script begins by importing necessary libraries and retrieving configuration parameters, including S3 bucket names, Redshift database credentials, and Glue job options.
python

### Retrieving Partition Information from Redshift: 
get_partitions_num_from_redshift(): <br>
Connects to an Amazon Redshift database and retrieves the number of partitions for specific tables storing Twitter data, such as users, tweets, and user followers.

### Retrieving Partition Information from S3: 
get_partitions_from_S3(): <br>
Scans the contents of an S3 bucket and categorizes partition keys based on their prefixes. It identifies partitions related to tweets, users, and user followers.

## Data Extraction and Transformation Functions:

create_DynamicFrame(partition: str) -> DynamicFrame: <br>
This function creates Glue DynamicFrames from data stored in Amazon S3 partitions.

write_DynamicFrame_to_s3(table: DynamicFrame, database: str, table_name: str) -> None: <br>
Writes a Glue DynamicFrame to an Amazon S3 bucket in Glue Parquet format.

get_data_users(data_catalog: str, table_name: str, s3_bucket: str, partitions: list, index: int) -> None: <br>
Functions retrieve, transform, and write data for users respectively. They use Glue DynamicFrames for processing and writing to S3.

get_data_followers(data_catalog: str, table_name: str, s3_bucket: str, partitions: list, index: int) -> None: <br>
Functions retrieve, transform, and write data for user followers respectively. They use Glue DynamicFrames for processing and writing to S3.

get_data_tweets(data_catalog: str, table_name: str, s3_bucket: str, partitions: list, index: int) -> None: <br>
Functions retrieve, transform, and write data for tweets respectively. They use Glue DynamicFrames for processing and writing to S3.

write_data_to_redshift(length: int, table_name: str, col_data: str) -> None: <br>
Writes data to an Amazon Redshift database table using Apache Spark. It creates a Spark DataFrame from the data and writes it to the specified Redshift table.

## Main Execution Logic: 
The script contains the main execution logic, which involves:

Comparing the number of partitions in Redshift with the number of partitions in S3 for users, user followers, and tweets.
If the numbers differ, the appropriate data extraction and transformation functions are called.
The transformed data is written to both Amazon S3 and Amazon Redshift.


## Conclusion
This ETL pipeline provides a robust solution for extracting, transforming, and loading Twitter data into Amazon Redshift and Amazon S3. It leverages AWS Glue and Apache Spark for efficient data processing and storage. It can be scheduled to run periodically to keep the data warehouse up-to-date with the latest Twitter data.