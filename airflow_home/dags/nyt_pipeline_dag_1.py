from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.tasks import get_articles, upload_to_gcs, read_from_gcs_and_load_duckdb
from scripts.sentiment_analysis import sentiment_analysis_task
import duckdb

# Define default args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

# Define the DAG
with DAG(
    'nyt_pipeline',
    default_args=default_args,
    description='Fetch NYT data, store in cloud storage, load to DuckDB, and \
        display stats in Streamlit',
    schedule_interval='@daily',  # Runs daily
    start_date=datetime(2024, 11, 15),
    catchup=False
) as dag:

    get_task = PythonOperator(
        task_id='get_articles',
        python_callable=get_articles,
    )

    upload_task = PythonOperator(
        task_id='upload_to_gcs',
        python_callable=lambda: upload_to_gcs('/tmp/nyt_articles.csv'),
    )

    load_to_duckdb_task = PythonOperator(
        task_id='load_to_duckdb',
        python_callable=read_from_gcs_and_load_duckdb,
    )   

    sentiment_task = PythonOperator(
        task_id='perform_sentiment_analysis',
        python_callable=sentiment_analysis_task,
    )


    # Task dependencies
    get_task >> upload_task >> load_to_duckdb_task >> sentiment_task
