## Airflow

Generate fernet key using below command

    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

Fernet key isn’t required but is best practice to use encrypted data when in a prod environment

Install apache-airflow using pip from https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html

    pip install "apache-airflow[celery]==2.9.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.1/constraints-3.8.txt"
    pip install apache-airflow-providers-docker

This installation is not required to run the project but for easier coding.

# Custom ELT Project

This repository contains a custom Extract, Load, Transform (ELT) project that utilizes Docker and PostgreSQL to demonstrate a simple ELT process.

## Repository Structure

1. **docker-compose.yaml**: This file contains the configuration for Docker Compose, which is used to orchestrate multiple Docker containers. It defines three services:
   - `source_postgres`: The source PostgreSQL database.
   - `destination_postgres`: The destination PostgreSQL database.
   - `elt_script`: The service that runs the ELT script.

2. **elt/Dockerfile**: This Dockerfile sets up a Python environment and installs the PostgreSQL client. It also copies the ELT script into the container and sets it as the default command.

3. **elt/elt_script.py**: This Python script performs the ELT process. It waits for the source PostgreSQL database to become available, then dumps its data to a SQL file and loads this data into the destination PostgreSQL database.

4. **source_db_init/init.sql**: This SQL script initializes the source database with sample data. It creates tables for users, films, film categories, actors, and film actors, and inserts sample data into these tables.

## How It Works

1. **Docker Compose**: Using the `docker-compose.yaml` file, three Docker containers are spun up:
   - A source PostgreSQL database with sample data.
   - A destination PostgreSQL database.
   - A Python environment that runs the ELT script.

2. **ELT Process**: The `elt_script.py` waits for the source PostgreSQL database to become available. Once it's available, the script uses `pg_dump` to dump the source database to a SQL file. Then, it uses `psql` to load this SQL file into the destination PostgreSQL database.

3. **Database Initialization**: The `init.sql` script initializes the source database with sample data. It creates several tables and populates them with sample data.