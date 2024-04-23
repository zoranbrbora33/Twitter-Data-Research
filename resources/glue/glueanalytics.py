import psycopg2
import boto3
import pandas as pd
import logging
import sys

# Configure the logging module
logger = logging.getLogger('imdb_ingestion')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

# Define the connection parameters for your Redshift cluster
redshift_params = {
    'host': 'admin-academy-redshift.c76boardkpkb.eu-central-1.redshift.amazonaws.com',
    'port': 5439,
    'database': 'twitter_redshift_db',
    'user': 'admin',
    'password': 'Academy2023!'
}

s3_client = boto3.client("s3")
s3_bucket = 'tara-academy-data'
object_key = 'european-cities.csv'

file_content = s3_client.get_object(Bucket=s3_bucket, Key=object_key)
df = pd.read_csv(file_content['Body'], sep=',')

table_names =  ['table1','table2','table3']


# Create a dictionary to store the city-country mapping
city_to_country = {}
for index, row in df.iterrows():
    city_to_country[row['grad']] = row['country']
    city_to_country[row['city']] = row['country']

# Create a list of cities from your CSV, combining "grad" and "city"
cities = df['grad'].combine_first(df['city']).tolist()

# Create a dictionary to store the counts for cities for each month
month_city_count_dict = {month: {city: 0 for city in cities} for month in range(1, 13)}

# Create a dictionary to store the total counts for cities for the entire year
total_city_count_dict = {city: 0 for city in cities}


# Establish a connection to Redshift
logging.info("Connecting to Redshift...")
conn = psycopg2.connect(**redshift_params)
for i in range(3):
    # Create a cursor
    cur = conn.cursor()

    for month in range(1, 13):
        # Construct the month pattern like '%-01-%', '%-02-%', ..., '%-12-%'
        month_pattern = f'%-{month:02d}-%'
        sql_query = [
                    f"""SELECT t.full_text FROM "twitter_redshift_db"."tara_academy_redshift"."tweets" t 
                        INNER JOIN "twitter_redshift_db"."tara_academy_redshift"."users"  u
                        ON t.user_id = u.user_id WHERE u.followers_count > 5000 AND t.created_at LIKE '{month_pattern}';""",
                    f"""SELECT DISTINCT
                                        tt.full_text,
                                        SUM(tt.in_retweet_cnt  + tt.in_quote_cnt + tt.in_reply_cnt) AS engagment
                                        FROM "twitter_redshift_db"."tara_academy_redshift"."users" AS tu
                                        INNER JOIN "twitter_redshift_db"."tara_academy_redshift"."tweets" AS tt
                                        ON tu.user_id = tt.user_id
                                        WHERE tu.is_croatian = True
                                        AND tt.created_at LIKE \'{month_pattern}\'
                                        AND tu.description LIKE '%travel%'
                                        AND tu.followers_count > 100
                                        AND (tt.full_text LIKE '%travel%' OR tt.full_text LIKE '%driving%' OR tt.full_text LIKE '%fly%' OR tt.full_text LIKE '%ride%' OR tt.full_text LIKE '%sail%' OR tt.full_text LIKE '%sightseeing%' OR tt.full_text LIKE '%tour%' OR tt.full_text LIKE '%trip%' OR tt.full_text LIKE '%cruising%' OR tt.full_text LIKE '%expedition%' OR tt.full_text LIKE '%touring%' OR tt.full_text LIKE '%wanderlust%' OR tt.full_text LIKE '%wandering%' OR tt.full_text LIKE '%trekking%' OR tt.full_text LIKE '%cruise%' OR tt.full_text LIKE '%sail%' OR tt.full_text LIKE '%explore%' OR tt.full_text LIKE '%sightsee%' OR tt.full_text LIKE '%abroad%' OR tt.full_text LIKE '%camping%' OR tt.full_text LIKE '%journey%' OR tt.full_text LIKE '%putovanj%'
                                        OR tt.full_text LIKE '%obilazak%' OR tt.full_text LIKE '%posjeta%' OR tt.full_text LIKE '%krstarenje%' OR tt.full_text LIKE '%ljetovanje%' OR tt.full_text LIKE '%lutanje%'
                                        OR tt.full_text LIKE '%odredište%' OR tt.full_text LIKE '%zimovanje%' OR tt.full_text LIKE '%logorovanje%' OR tt.full_text LIKE '%skijanje%' OR tt.full_text LIKE '%izlet%'
                                        OR tt.full_text LIKE '%planinarenje%')
                                        OR tu.description LIKE 'blog%'
                                        AND tu.screen_name NOT IN ('eZadar', 'DubrovnikTB', 'FindCroatia', 'Rovinj_official', 'TheHDTravels', 'SecretDalmatia', 'LyndaMilina', 'latcroatia', 'tourguidesplit', 'Dubrovnik_',
                                        'tourdalmatia', 'aslagency', 'Travel2Ultra', 'Croatia_Charter', 'CroatiaFerries', 'Islandoflosinj', 'LuxuryCroatia', 'ZagrebTravels')
                                        GROUP BY tt.full_text, tu.followers_count
                                        ORDER BY engagment DESC""",
                    f"""SELECT t.full_text
                                    FROM "twitter_redshift_db"."tara_academy_redshift".users u
                                    JOIN "twitter_redshift_db"."tara_academy_redshift".tweets t
                                    ON u.user_id = t.user_id
                                    AND u.screen_name IN ('Perkz', 'Sandra_Ri051', 'KolindaGK', 'KarloBujan', 'knoll_doll', 'ivospigel', 'SeverMaja', 'kmacan', 'natasazecevic', 'domagojsever')
                                    AND t.created_at LIKE \'{month_pattern}\'
                                    ORDER BY u.followers_count DESC;"""
                    ]
        # Execute a query to select the full_text column for the specific month
        logging.info(f"Executing query for month {month}...")
        cur.execute(sql_query[i])
        
        # Fetch all rows from the result
        rows = cur.fetchall()
        
        # Iterate through the rows and count the occurrences of cities for the specific month
        for row in rows:
            full_text = row[0].lower()  # Convert to lowercase for case-insensitive matching
            
            for city in cities:
                if city.lower() in full_text:
                    month_city_count_dict[month][city] += 1
                    total_city_count_dict[city] += 1

    # Create a list to store the data for the Redshift table
    table_data = []

    for city in cities:
        country = city_to_country.get(city, 'Unknown Country')
        
        # Check if the city exists in either the "grad" or "city" column
        grad_match = df[df['grad'] == city]
        city_match = df[df['city'] == city]

        if not grad_match.empty:
            grad = grad_match['grad'].values[0]
            city_name = grad_match['city'].values[0]
        elif not city_match.empty:
            grad = city_match['grad'].values[0]
            city_name = city_match['city'].values[0]
        else:
            grad = 'Unknown Grad'
            city_name = 'Unknown City'

        row_data = [grad, city_name, country]  # Include "grad" and "city" in the row

        # Append mentions for each month and total mentions
        for month in range(1, 13):
            row_data.append(month_city_count_dict[month][city])

        row_data.append(total_city_count_dict[city])

        table_data.append(row_data)

    # Define the name of the table you want to create
    table_name = table_names[i]

    # Drop the table if it exists
    drop_table_sql = f"""
    DROP TABLE IF EXISTS "twitter_redshift_db"."tara_academy_redshift"."{table_name}";
    """

    # Execute the drop table SQL command
    cur.execute(drop_table_sql)
    conn.commit()

    # Define the SQL command to create the Redshift table within the specified schema
    logging.info("Creating the table in Redshift...")
    create_table_sql = f"""
    CREATE TABLE "twitter_redshift_db"."tara_academy_redshift"."{table_name}" (
        grad VARCHAR(255),
        city VARCHAR(255),
        country VARCHAR(255),
        january INT,
        february INT,
        march INT,
        april INT,
        may INT,
        june INT,
        july INT,
        august INT,
        september INT,
        october INT,
        november INT,
        december INT,
        total_mentions INT
    );
    """

    # Execute the create table SQL command
    cur.execute(create_table_sql)

    # Define the SQL command to insert data into the Redshift table
    batch_size = 100000  # You can adjust this based on your requirements

    # Batch insert data into the Redshift table
    logging.info("Inserting data into the table...")
    insert_data_sql = f"""
        INSERT INTO "twitter_redshift_db"."tara_academy_redshift"."{table_name}"
        (grad, city, country, january, february, march, april, may, june, july, august, september, october, november, december, total_mentions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        for i in range(0, len(table_data), batch_size):
            batch = table_data[i:i + batch_size]
            cur.executemany(insert_data_sql, batch)
            conn.commit()

        logging.info("Table creation and data insertion completed successfully.")

    except Exception as e:
        logging.error("Error:", e)
    finally:
        # Close the cursor and the connection
        cur.close()
conn.close()
    
