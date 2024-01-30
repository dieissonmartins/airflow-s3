from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

# Define the list of tasks or configurations for your DAGs
dag_configurations = [
    {
        "dag_id": "VISOES_BI",
        "schedule_interval": "0 0 * * *",
        "tasks": [
            {
                "task_id": "VISOES_BI_TASK",
                "params": "bancos=db_ovosjosidith_qa"
            },
            {
                "task_id": "VISOES_BI_TASK2",
                "params": "bancos=db_ultracheese,web68db3 dt_ini=D-1 dt_fim=D-1"
            }
        ]
    },
    {
        "dag_id": "BI_FORM_ATENDIMENTO",
        "schedule_interval": "0 0 * * *",
        "tasks": [
            {
                "task_id": "BI_FORM_ATENDIMENTO_TASK",
                "params": "bancos=db_ovosjosidith_qa"
            },
            {
                "task_id": "BI_FORM_ATENDIMENTO_TASK2",
                "params": "bancos=db_ultracheese,web68db3 dt_ini=D-1 dt_fim=D-1"
            }
        ]
    },
    {
        "dag_id": "VISOES_BI",
        "schedule_interval": "0 0 * * *",
        "tasks": [
            {
                "task_id": "VISOES_BI_TASK",
                "params": "bancos=db_ovosjosidith_qa"
            },
            {
                "task_id": "VISOES_BI_TASK2",
                "params": "bancos=db_ultracheese,web68db3 dt_ini=D-1 dt_fim=D-1"
            }
        ]
    },
    {
        "dag_id": "ATUALIZA_FETCHED_FORM_VENCIMENTO",
        "schedule_interval": "0 0 * * *",
        "tasks": [
            {
                "task_id": "ATUALIZA_FETCHED_FORM_VENCIMENTO_TASK",
                "params": "bancos=db_ovosjosidith_qa"
            },
            {
                "task_id": "ATUALIZA_FETCHED_FORM_VENCIMENTO_TASK2",
                "params": "bancos=db_ultracheese,web68db3 dt_ini=D-1 dt_fim=D-1"
            }
        ]
    }
]


# Define a function to create DAGs dynamically
def create_dag(dag_id, schedule_interval, tasks):
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

    for task_configuration in tasks:
        task_id = task_configuration['task_id']

        # Define tasks for each DAG
        DummyOperator(task_id=task_id, dag=dag)

    return dag


# Iterate through the configurations and create DAGs
for config in dag_configurations:
    dag_id = config["dag_id"]
    schedule_interval = config["schedule_interval"]
    tasks = config["tasks"]

    # Call the create_dag function to create the DAG dynamically
    globals()[dag_id] = create_dag(dag_id, schedule_interval, tasks)
