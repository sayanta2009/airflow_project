FROM apache/airflow:slim-2.9.2rc1-python3.11

RUN pip install apache-airflow-providers-docker
