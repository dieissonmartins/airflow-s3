from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from airflow.operators.bash import BashOperator

# Define your ECS task parameters
task_definition = "4e88e5f4144c42e9910ea994a28eef3f"
ecs_cluster = "airflow-ecs"
php_script_path_on_container = "/scripts/index.php"
ecs_subnets = ["subnet-03e9ed8201ae37039"]

# Define your DAG parameters
default_args = {
    'owner': 'Dieisson',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ECS_RUN_TASK_OPERATOR',
    default_args=default_args,
    schedule="*/5 * * * *"
)

run_task = EcsRunTaskOperator(
    task_id="ECS_RUN_TASK_OPERATOR",
    cluster=ecs_cluster,
    task_definition=task_definition,
    overrides={
        'containerOverrides': [
            {
                'name': 'run-airflow-ecr',
                'command': ['/usr/bin/php', php_script_path_on_container],
            },
        ],
    },
    network_configuration={"awsvpcConfiguration": {"subnets": ecs_subnets}},
    dag=dag
)

run_task
