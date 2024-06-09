import os
import subprocess
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}


def run_elt_script():
    script_path = "/opt/airflow/elt/elt_script.py"
    result = subprocess.run(
        ["python", script_path], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            f"Script failed with error: {result.stderr}"
        )
    else:
        print(result.stdout)


dag = DAG(
    "elt_and_dbt",
    default_args=default_args,
    description="An ELT workflow with dbt",
    start_date=datetime(2023, 10, 3),
    catchup=False,
)

t1 = PythonOperator(
    task_id="run_elt_script",
    python_callable=run_elt_script,
    dag=dag,
)

t2 = DockerOperator(
    task_id="dbt_run",
    image="ghcr.io/dbt-labs/dbt-postgres:1.4.7",
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt",
        "--full-refresh",
    ],
    auto_remove=True,
    # socket we opened
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(
            source=os.getenv("DBT_PROJECT_DIR"),
            target="/dbt",
            type="bind",
        ),
        Mount(
            source=os.getenv("DBT_SOURCE_DIR"),
            target="/root",
            type="bind",
        ),
    ],
    dag=dag,
)

# task t2 is followed by t1
t1 >> t2
