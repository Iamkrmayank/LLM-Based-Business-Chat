import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

def create_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        sslmode="require"
    )
    return conn

def create_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS verified_data (
            id SERIAL PRIMARY KEY,
            name TEXT,
            address TEXT,
            website TEXT,
            phone_number TEXT,
            reviews BIGINT,
            rating FLOAT,
            latitude FLOAT,
            longitude FLOAT,
            status TEXT,
            verified_at TIMESTAMP DEFAULT NOW()
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_data(name, address, website, phone_number, reviews, rating, latitude, longitude, status):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO verified_data (name, address, website, phone_number, reviews, rating, latitude, longitude, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    ''', (name, address, website, phone_number, reviews, rating, latitude, longitude, status))
    conn.commit()
    cur.close()
    conn.close()

def fetch_all_data():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM verified_data;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows