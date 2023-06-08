import json
import psycopg2

def establish_connection():
    # Load the configuration from the file
    with open('config.config', 'r') as f:
        config = json.load(f)

    # Extract the required values from the config dictionary
    db_name = config['db_name']
    db_user = config['db_user']
    pw = config['pw']
    host = config['host']
    port = config['port']

    # Establish the PostgreSQL connection
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=db_name,
        user=db_user,
        password=pw,
        options="-c client_encoding=UTF-8"
    )

    return conn
