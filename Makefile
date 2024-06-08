install: # Install dependencies
	@python -m pip install -U pip
	@pip install -U poetry
	@poetry install --no-root

run: # run command destination database
	@docker exec -it airflow_project-destination_postgres-1 psql -U postgres

lint: # code formatting and linting
	@pre-commit run --all-files
