import boto3
import psycopg2
import os
import json

def lambda_handler(event, context):
    # Define configuration parameters
    s3_bucket = 'tara-academy-data' # Amazon S3 bucket where data is stored
    sql_script_key = 'create_schema.sql' # Key for an SQL script (not used in this code)
    redshift_cluster_endpoint = 'admin-academy-redshift.c76boardkpkb.eu-central-1.redshift.amazonaws.com' # Redshift cluster endpoint
    redshift_db_name = 'twitter_redshift_db' # Redshift database name
    redshift_user = 'admin' # Redshift username
    redshift_password = 'Academy2023!' # Redshift password
    
    # Initialize Redshift connection
    conn = psycopg2.connect(
    host='admin-academy-redshift.c76boardkpkb.eu-central-1.redshift.amazonaws.com',
    port=5439,
    dbname='twitter_redshift_db',
    user='admin',
    password='Academy2023!'
    )

    # Create Redshift schema if it doesn't exist
    create_schema_query = 'CREATE SCHEMA IF NOT EXISTS "tara_test";'
    cur = conn.cursor()
    cur.execute(create_schema_query)
    conn.commit()

    # Truncate (clear) tables to prepare for data loading
    truncate_table_users='TRUNCATE TABLE "tara_s3_to_redshift_database_schema"."users";'
    truncate_table_user_followers='TRUNCATE TABLE "tara_s3_to_redshift_database_schema"."user_followers";'
    truncate_table_tweets='TRUNCATE TABLE "tara_s3_to_redshift_database_schema"."tweets";'
    cur = conn.cursor()
    cur.execute(truncate_table_users)
    conn.commit()
    cur.execute(truncate_table_user_followers)
    conn.commit()
    cur.execute(truncate_table_tweets)
    conn.commit()

    # Create or replace 'users' table schema
    cur = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS "tara_test"."users" (
    "user_id" BIGINT,
    "name" VARCHAR(600),
    "screen_name" VARCHAR(600),
    "location" VARCHAR(600),
    "description" VARCHAR(600),
    "protected" BOOLEAN,
    "followers_count" BIGINT,
    "friends_count" BIGINT,
    "statuses_count" BIGINT,
    "is_croatian" BOOLEAN,
    "clean_location" VARCHAR(600)
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    
    # COPY data from S3 to 'users' table
    copy_query = '''
    COPY tara_test.users
    FROM 's3://tara-academy-data/datalake/users/'
    IAM_ROLE 'arn:aws:iam::456582705970:role/RedshiftRole'
    FORMAT AS PARQUET;
    '''
    cur.execute(copy_query)
    conn.commit()
    
    # Create or replace 'user_followers' table schema
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS "tara_test"."user_followers" (
        "user_id" varchar(600),
        "followers_string" varchar(6000)
    ); 
    '''
    cur.execute(create_table_query)
    conn.commit()
    
    # COPY data from S3 to 'user_followers' table
    copy_query = '''
    COPY tara_test.user_followers
    FROM 's3://tara-academy-data/datalake/user_followers/'
    IAM_ROLE 'arn:aws:iam::456582705970:role/RedshiftRole'
    FORMAT AS PARQUET;
    '''
    cur.execute(copy_query)
    conn.commit()
    
    # Create or replace 'tweets' table schema
    create_table_query = """
    CREATE TABLE IF NOT EXISTS "tara_test"."tweets" (
    "id" BIGINT,
    "created_at" TIMESTAMP,
    "user_id" BIGINT,
    "full_text" VARCHAR(8000),
    "lang" VARCHAR(600),
    "hashtags" VARCHAR(600),
    "user_mentions" VARCHAR(1200),
    "is_retweet" BOOLEAN,
    "in_retweet_cnt" FLOAT,
    "retweet_created_at" VARCHAR(600),
    "retweet_from_user_id" BIGINT,
    "retweet_from_status_id" BIGINT,
    "is_quote" BOOLEAN,
    "in_quote_cnt" FLOAT,
    "quote_created_at" VARCHAR(600),
    "quote_timedelta_sec" BIGINT,
    "quote_from_user_id" BIGINT,
    "quote_from_status_id" BIGINT,
    "is_reply" BOOLEAN,
    "in_reply_cnt" BIGINT,
    "in_reply_to_user_id" BIGINT,
    "in_reply_to_status_id" BIGINT
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    
    # COPY data from S3 to 'tweets' table
    copy_query ='''
    COPY tara_test.tweets
    FROM 's3://tara-academy-data/datalake/tweets/'
    IAM_ROLE 'arn:aws:iam::456582705970:role/RedshiftRole'
    FORMAT AS PARQUET;
    '''
    cur.execute(copy_query)
    conn.commit()

    # Close the database connection
    conn.close()

    # Return a response indicating successful execution
    return {
        'statusCode': 200,
        'body': json.dumps("Database and schema creation complete.")
    }
