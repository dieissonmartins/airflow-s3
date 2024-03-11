from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
import mysql.connector


def get_dags():
    config = {
        'host': 'airflow.chtfkeaqrbrm.us-east-1.rds.amazonaws.com',
        'user': 'dieisson',
        'password': '12345678',
        'database': 'airflow',
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = '''
        SELECT a.id                as 'dag_id'
             , a.name              as 'dag_name'
             , a.schedule_interval as 'schedule_interval'
             , b.id                as 'task_id'
             , b.name              as 'task_name'
             , b.params            as 'params'
        FROM dags a
                 JOIN tasks b ON (b.dag_id = a.id)
        ORDER BY a.id, b.`order`
    '''

    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    dags = {}
    for row in results:
        row_dict = dict(zip(columns, row))

        dag_name = row_dict['dag_name']
        task_name = row_dict['task_name']
        params = row_dict['params']
        schedule_interval = row_dict['schedule_interval']

        dag_key = (str(dag_name))
        if dag_key not in dags:
            dags[dag_key] = {
                'dag_id': dag_name,
                'schedule_interval': schedule_interval,
                'tasks': {}
            }

        task_key = (str(dag_name) + str('_') + str(task_name))
        if task_key not in dags[dag_key]['tasks']:
            dags[dag_key]['tasks'][task_key] = {
                'task_id': task_name,
                'params': params
            }

    response = dags

    return response


def create_dag(dag_id, schedule_interval, tasks):
    default_args = {
        'owner': 'Dieisson',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
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

    task_configuration = next(iter(tasks.values()))
    task_configuration_key = next(iter(tasks.keys()))
    tasks.pop(task_configuration_key)

    previous_task = create_task(dag, task_configuration['task_id'])

    for task_configuration in tasks.values():
        task_id = task_configuration['task_id']
        # params = task_configuration['params']

        task = create_task(dag, task_id)
        previous_task >> task
        previous_task = task

    return dag


def create_task(dag, task_id):
    return DummyOperator(task_id=task_id, dag=dag)


#dags = get_dags()
dags = {}

# Iterate through the configurations and create DAGs
for dag in dags.values():
    dag_id = dag["dag_id"]
    schedule_interval = dag["schedule_interval"]
    tasks = dag["tasks"]

    new_dag = create_dag(dag_id, schedule_interval, tasks)
    globals()[dag_id] = new_dag
