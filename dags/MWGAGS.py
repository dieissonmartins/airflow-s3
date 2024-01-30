from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

# Define the list of tasks or configurations for your DAGs
dag_configurations = [
    {"dag_id": "VISOES_BI", "schedule_interval": "0 0 * * *"},
    {"dag_id": "BI_FORM_ATENDIMENTO", "schedule_interval": "0 2 * * *"},
    {"dag_id": "VISOES_BI", "schedule_interval": "0 2 * * *"},
    {"dag_id": "ATUALIZA_FETCHED_FORM_VENCIMENTO", "schedule_interval": "0 2 * * *"},
    {"dag_id": "BARCODE_TIROLEZ", "schedule_interval": "0 2 * * *"},
    {"dag_id": "ALERTA_RUPTURA", "schedule_interval": "0 2 * * *"}
]


# Define a function to create DAGs dynamically
def create_dag(dag_id, schedule_interval):
    default_args = {
        'owner': 'Dieisson',
        'depends_on_past': False,
        'start_date': datetime(2022, 1, 1),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    dag = DAG(
        dag_id=dag_id,
        default_args=default_args,
        description=f'Dynamic DAG {dag_id}',
        schedule_interval=schedule_interval,
    )

    # Define tasks for each DAG
    DummyOperator(task_id='task', dag=dag)

    return dag


# Iterate through the configurations and create DAGs
for config in dag_configurations:
    dag_id = config["dag_id"]
    schedule_interval = config["schedule_interval"]

    # Call the create_dag function to create the DAG dynamically
    globals()[dag_id] = create_dag(dag_id, schedule_interval)
