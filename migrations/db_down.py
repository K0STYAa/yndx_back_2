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

cur.execute('DROP TABLE IF EXISTS files;')

conn.commit()

cur.close()
conn.close()
