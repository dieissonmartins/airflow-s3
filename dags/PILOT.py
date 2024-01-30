from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'Dieisson',
    'depends_on_past': False,
}

dag = DAG(
    "PILOT",
    description="PILOT execução DAGs deploy S3",
    default_args=default_args,
    schedule="*/5 * * * *",
    tags=['Github Actions', 's3'],
    catchup=False,
    start_date=datetime(2024, 1, 1)
)


def run():
    print('Executando Pilot...')


run = PythonOperator(
    task_id="run_pilot",
    python_callable=run,
    dag=dag
)

run_bash = BashOperator(
    task_id="run_pilot_bash",
    bash_command="echo 'runting process...'",
    dag=dag
)

run >> run_bash


dag2 = DAG(
    "PILOT2",
    description="PILOT execução DAGs deploy S3",
    default_args=default_args,
    schedule="*/5 * * * *",
    tags=['Github Actions', 's3'],
    catchup=False,
    start_date=datetime(2024, 1, 1)
)


run_bash2 = BashOperator(
    task_id="run_pilot_bash2",
    bash_command="echo 'runting process2...'",
    dag=dag2
)

run_bash2