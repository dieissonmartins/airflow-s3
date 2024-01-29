from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.operators.ecs_api import ECSOperator

# Define your ECS task parameters
ecs_task_definition_arn = "4e88e5f4144c42e9910ea994a28eef3f"
ecs_cluster = "airflow-ecs"
ecs_subnets = ["subnet-03e9ed8201ae37039"]
ecs_security_groups = ["sg-0f2a7cbfdf97d7dd2"]
php_script_path_on_container = "/scripts/index.php"

# Define your DAG parameters
default_args = {
    'owner': 'Dieisson',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ecs_php_script_dag',
    default_args=default_args,
    schedule="*/5 * * * *",  # You can adjust the schedule as needed
)

# Define your ECS task
ecs_task = ECSOperator(
    task_id='ecs_php_script_task',
    task_definition=ecs_task_definition_arn,
    cluster=ecs_cluster,
    launch_type='FARGATE',  # or 'EC2' based on your setup
    network_configuration={
        'awsvpcConfiguration': {
            'subnets': ecs_subnets,
            'securityGroups': ecs_security_groups,
        },
    },
    overrides={
        'containerOverrides': [
            {
                'name': 'run-airflow-ecr',  # Replace with your container name
                'command': ['/usr/bin/php', php_script_path_on_container],
            },
        ],
    },
    aws_conn_id='aws_conn_ecs',
    dag=dag,
)

# Set task dependencies as needed
ecs_task
