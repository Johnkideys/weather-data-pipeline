import os
import pandas as pd
import duckdb
from google.cloud import storage
from dotenv import load_dotenv
from .get_data_nyt import get_news_call

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

def get_articles():
    df = get_news_call()
    file_path = '/tmp/nyt_articles.csv'
    df.to_csv(file_path, index=False)
    print(f"Articles saved to {file_path}")
    return file_path

def upload_to_gcs(file_path):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob('nyt_articles.csv')
    blob.upload_from_filename(file_path)
    print(f"CSV uploaded to GCS as 'nyt_articles.csv'")

def read_from_gcs_and_load_duckdb():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob('nyt_articles.csv')
    local_path = '/tmp/nyt_articles_from_gcs.csv'
    blob.download_to_filename(local_path)

    # Connect to DuckDB
    conn = duckdb.connect('nyt_warehouse.db')
    

    # Create table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS nyt_articles (
            article_id VARCHAR PRIMARY KEY,
            pub_date TIMESTAMP,
            headline TEXT,
            lead_paragraph TEXT,
            section TEXT,
            subsection TEXT,
            web_url TEXT,
            keywords TEXT,
            word_count INTEGER,
            sentiment VARCHAR 
        );
    """)

    # Load data into DuckDB
    df = pd.read_csv(local_path)

    conn.register("temp_table", df)
    #conn.execute("INSERT INTO nyt_articles SELECT * FROM temp_table;")
    conn.execute("""
    INSERT OR REPLACE INTO nyt_articles (
        article_id, pub_date, headline, lead_paragraph, section,
        subsection, web_url, keywords, word_count
    )
    SELECT article_id, pub_date, headline, lead_paragraph, section,
           subsection, web_url, keywords, word_count
    FROM temp_table;
    """)
    print("Data loaded into DuckDB from GCS.")
    conn.close()
