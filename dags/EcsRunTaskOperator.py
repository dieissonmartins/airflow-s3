from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from datetime import datetime, timedelta

# Define your ECS task parameters
ecs_cluster = "airflow-ecs"
task_definition = "task-definition-apacheairflow:1"
ecs_subnets = ["subnet-01e897958bf6fe9a5"]

dag = DAG(
    'ECS_RUN_TASK_OPERATOR',
    default_args={
        'owner': 'Dieisson',
        'start_date': datetime(2024, 3, 11),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    schedule="@hourly",
)

run_task = EcsRunTaskOperator(
    task_id="ECS_RUN_TASK_OPERATOR",
    cluster=ecs_cluster,
    task_definition=task_definition,
    launch_type='FARGATE',
    overrides={
        'containerOverrides': [
            {
                'name': 'airflow-ecr',
                "command": ["php", "scripts/index.php"],
            },
        ],
    },
    network_configuration={"awsvpcConfiguration": {"subnets": ecs_subnets}},
    aws_conn_id='aws_conn_ecs',
    dag=dag
)

run_task
