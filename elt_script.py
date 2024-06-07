import subprocess
import time
import logging


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        # logging.FileHandler(LOGS_DIR.joinpath(f"logging_{today_date}.log"), mode="w+"), 
        logging.StreamHandler()],
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

log = logging.getLogger(__name__)


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    retries = 0
    log.info("Waiting for postgres host %s", host)
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                log.info("Successfully connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            log.error(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            log.info(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    log.critical("Max retries reached. Exiting.")
    return False


# Use the function before running the ELT process
if not wait_for_postgres(host="source_postgres"):
    exit(1)

log.info("Starting ELT script...")

# Configuration for the source PostgreSQL database
source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    # Use the service name from docker-compose as the hostname
    'host': 'source_postgres'
}

# Configuration for the destination PostgreSQL database
destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    # Use the service name from docker-compose as the hostname
    'host': 'destination_postgres'
}

# Use pg_dump to dump the source database to a SQL file
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'  # Do not prompt for password
]

# Set the PGPASSWORD environment variable to avoid password prompt
subprocess_env = dict(PGPASSWORD=source_config['password'])

# Execute the dump command
try:
    subprocess.run(dump_command, env=subprocess_env, check=True)
except subprocess.CalledProcessError as e:
    log.error(f"Error connecting to PostgreSQL: {e}")
    exit(1)

# Use psql to load the dumped SQL file into the destination database
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql'
]

# Set the PGPASSWORD environment variable for the destination database
subprocess_env = dict(PGPASSWORD=destination_config['password'])

# Execute the load command
subprocess.run(load_command, env=subprocess_env, check=True)

log.info("Ending ELT script...")