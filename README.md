# ELT Project using Airflow, DBT and Postgres

This repository contains a custom Extract, Load, Transform (ELT) project that utilizes Airflow, PostgreSQL and DBT to demonstrate a simple ELT process.

## Repository Structure

1. **docker-compose.yaml**: This file contains the configuration for Docker Compose, which is used to orchestrate multiple Docker containers. It defines three services:
   - `source_postgres`: The source PostgreSQL database.
   - `destination_postgres`: The destination PostgreSQL database.
   - `airflow`: The webserver and scheduler.

2. **elt/Dockerfile**: This Dockerfile sets up a Python environment and installs the PostgreSQL client. It also copies the ELT script into the container and sets it as the default command.

3. **elt/elt_script.py**: This Python script performs the ELT process. It waits for the source PostgreSQL database to become available, then dumps its data to a SQL file and loads this data into the destination PostgreSQL database.

4. **source_db_init/init.sql**: This SQL script initializes the source database with sample data. It creates tables for users, films, film categories, actors, and film actors, and inserts sample data into these tables.

## How It Works

1. **Docker Compose**: Using the `docker-compose.yaml` file, three Docker containers are spun up:
   - A source PostgreSQL database with sample data.
   - A destination PostgreSQL database.
   - An airflow webserver and scheduler that consists of two tasks in a single DAG - firstly to copy the tables from source db to
   destination db and, secondly run some DBT macros to create additional tables

2. **Database Initialization**: The `init.sql` script initializes the source database with sample data. It creates several tables and populates them with sample data.

# Installation

Create a Python virtualenv, activate it and run the below command

    make install

### DBT

Create  ~/.dbt/profiles.yml file with below content 

    custom_postgres:
        outputs:
            dev:
            dbname: destination_db
            host: host.docker.internal
            pass: secret
            port: 5434
            schema: public
            threads: 1
            type: postgres
            user: postgres
        target: dev

### Airflow

Generate fernet key using below command and put in your `.env` file

    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

Fernet key isn’t required but is best practice to use encrypted data when in a prod environment

`This installation is not required to run the project but for easier coding.` Install apache-airflow using pip from https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html

    pip install "apache-airflow[celery]==2.9.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.1/constraints-3.8.txt"
    pip install apache-airflow-providers-docker

# How to run

- Use `docker-compose up` to churn up all the containers
- Once all the containers are up and running, go to `http://webserver.airflow-project.orb.local/home` and login in with airflow username and password set in .env file
- Run the dag `elt_and_dbt`
- Run `make run` to connect to the destination postgres db
    - Use `\c destination_db` to connect to the database
    - Use `\dt` to list all the tables migrated from source database and those created by DBT

