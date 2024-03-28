from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from datetime import datetime, timedelta

# Define your ECS task parameters
ecs_cluster = "generate-pptx"
task_definition = "spire-presentation-mw-generate-pptx:3"
ecs_subnets = ["subnet-01e897958bf6fe9a5"]

dag = DAG(
    'GERAR_PPTX_DAG_3',
    default_args={
        'owner': 'Dieisson',
        'start_date': datetime(2024, 3, 11),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    schedule=None
)

run_task = EcsRunTaskOperator(
    task_id="GERAR_PPTX_DAG_3",
    cluster=ecs_cluster,
    task_definition=task_definition,
    launch_type='FARGATE',
    overrides={
        'containerOverrides': [
            {
                'name': 'spire-presentation-mw',
                "command": ["python", "main.py"],
            },
        ],
    },
    network_configuration={"awsvpcConfiguration": {"subnets": ecs_subnets}},
    aws_conn_id='aws_conn_ecs',
    dag=dag
)

run_task
