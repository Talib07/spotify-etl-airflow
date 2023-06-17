from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from Spotify_ETL import populate_data

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'start_date' : datetime(2023,6,15),
    'email' : ['airflow@example.com'],
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes=1)
}

dag = DAG(
    'Spotify_DAG',
    default_args = default_args,
    description = 'First ETL Code'
)

run_etl = PythonOperator(
    task_id = 'Complete_spotify_ETL',
    python_callable = populate_data,
    dag = dag
)

run_etl


