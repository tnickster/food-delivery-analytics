from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='food_delivery_pipeline',
    start_date=datetime(2026, 3, 23),
    schedule_interval='@daily',
    catchup=False,
    tags=['food_delivery'],
) as dag:
    
    # Task 1: Extract data to BigQuery
    extract = BashOperator(
        task_id='extract_data',
        bash_command='python /opt/airflow/scripts/extract_data.py',
    )
    
    # Task 2: Run dbt models
    transform = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir /opt/airflow/dbt',
    )
    
    # Set dependencies
    extract >> transform