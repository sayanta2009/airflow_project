FROM python:3.11-slim

# COPY pyproject.toml poetry.lock ./

# Install PostgreSQL command-line tools
RUN apt update && apt -y install postgresql-client && apt-get clean
    # && pip install -U poetry \
    # && python -m venv .venv \
    # && poetry install --no-root

# Copy the ELT script
COPY elt_script.py .

# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]
