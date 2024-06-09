FROM apache/airflow:latest

RUN pip install apache-airflow-providers-docker psycopg2-binary

RUN airflow db upgrade
