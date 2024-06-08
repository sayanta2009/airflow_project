FROM python:3.11-slim

# COPY pyproject.toml poetry.lock ./

# Install PostgreSQL command-line tools
RUN apt update && apt -y install postgresql-client && apt-get clean
    # && pip install -U poetry \
    # && python -m venv .venv \
    # && poetry install --no-root

COPY start.sh /app/start.sh
# Copy the ELT script
COPY elt_script.py .

WORKDIR /app

# CronJob - Run the script everyday at 03:00
RUN echo "0 3 * * * python /app/elt_script.py" | crontab - 

# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]
