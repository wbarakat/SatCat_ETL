import configparser
import sys
import pathlib
import psycopg2
from psycopg2 import sql

"""
Part of DAG that connects to Redshift, creates table and copies data over from S3
"""

# Load AWS credentials
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.resolve()
config_file = "configuration.conf"
parser.read(f"{script_path}/{config_file}")

# Define config variables
USERNAME = parser.get("aws_config", "redshift_username")
PASSWORD = parser.get("aws_config", "redshift_password")
HOST = parser.get("aws_config", "redshift_hostname")
PORT = parser.get("aws_config", "redshift_port")
REDSHIFT_ROLE = parser.get("aws_config", "redshift_role")
DATABASE = parser.get("aws_config", "redshift_database")
BUCKET_NAME = parser.get("aws_config", "bucket_name")
ACCOUNT_ID = parser.get("aws_config", "account_id")
TABLE_NAME = "spacetracker_satcat_data"

# Our S3 file & role_string
file_path = f"s3://{BUCKET_NAME}/spacetracker_satcat_data.csv"
role_string = f"arn:aws:iam::{ACCOUNT_ID}:role/{REDSHIFT_ROLE}"

# Create Redshift table if it doesn't exist
sql_create_table = sql.SQL(
    """CREATE TABLE IF NOT EXISTS {table} (
                            ID integer,
                            OBJECT_TYPE varchar,
                            SATNAME varchar,
                            COUNTRY varchar,
                            LAUNCH date,
                            SITE varchar,
                            DECAY date,
                            PERIOD float,
                            INCLINATION float,
                            APOGEE float,
                            PERIGEE float,
                            LAUNCH_YEAR date,
                            LIFESPAN_DAYS integer
                        );"""
).format(table=sql.Identifier(TABLE_NAME))

# If ID already exists in table, we remove it and add new ID record during load.
create_temp_table = sql.SQL("CREATE TEMP TABLE our_staging_table (LIKE {table});").format(table = sql.Identifier(TABLE_NAME))
sql_copy_to_temp = f"COPY our_staging_table FROM '{file_path}' iam_role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV;"
delete_from_table = sql.SQL("DELETE FROM {table} USING our_staging_table WHERE {table}.id = our_staging_table.id;").format(table = sql.Identifier(TABLE_NAME))
insert_into_table = sql.SQL("INSERT INTO {table} SELECT * FROM our_staging_table;").format(table = sql.Identifier(TABLE_NAME))
drop_temp_table = "DROP TABLE our_staging_table;"

def main():
    """Upload file form S3 to Redshift Table"""
    #validate_input(output_name)
    rs_conn = connect_to_redshift()
    load_data_into_redshift(rs_conn)

def connect_to_redshift():
    """Connect to Redshift instance"""
    try:
        rs_conn = psycopg2.connect(dbname = DATABASE, user = USERNAME, password = PASSWORD, host = HOST, port = PORT)
        return rs_conn
    except Exception as e:
        print(f"Unable to connect to Redshift. Error {e}")
        sys.exit(1)

def load_data_into_redshift(rs_conn):
    """Load data from S3 into Redshift"""
    with rs_conn:

        cur = rs_conn.cursor()
        cur.execute(sql_create_table)
        cur.execute(create_temp_table)
        cur.execute(sql_copy_to_temp)
        cur.execute(delete_from_table)
        cur.execute(insert_into_table)
        cur.execute(drop_temp_table)

        # Commit only at the end, so we won't end up
        # with a temp table and deleted main table if something fails
        rs_conn.commit()

if __name__ == '__main__':
    main()
