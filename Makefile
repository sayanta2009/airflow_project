install: # Install dependencies
	@python -m pip install -U pip
	@pip install -U poetry
	@poetry install --no-root

run: # run command destination database, then use \c database name to use the database
	@docker exec -it airflow_project-destination_postgres-1 psql -U postgres

lint: # code formatting and linting
	@pre-commit run --all-files

airflow_init: # Initialize airflow user
	@docker-compose up init-airflow -d
