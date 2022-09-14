import os
from dotenv import load_dotenv
import psycopg2

def get_db_connection():

    load_dotenv("migrations/.env.migrations")

    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        port=os.getenv('POSTGRES_PORT'),
        user=os.getenv('POSTGRES_USERNAME'),
        password=os.getenv('POSTGRES_PASSWORD'))

    return conn

conn = get_db_connection()

cur = conn.cursor()

cur.execute("CREATE TABLE files (type varchar(10) CHECK (type = 'FOLDER' OR type = 'FILE'),"
                                   'url varchar(100),'
                                   'id varchar(40) PRIMARY KEY,'
                                   'size integer CHECK (size >= 0),'
                                   'parentId varchar(40),'
                                   'date timestamp DEFAULT CURRENT_TIMESTAMP,'
                                   "children varchar(40)[] DEFAULT '{}');"
                                   )

conn.commit()

cur.close()
conn.close()
