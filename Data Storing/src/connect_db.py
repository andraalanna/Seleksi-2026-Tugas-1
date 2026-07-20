import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file automatically
load_dotenv(find_dotenv())

def get_db_params(dbname_override=None):
    params = {
        "dbname": os.getenv("DB_NAME", "ck3_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432")
    }
    if dbname_override:
        params["dbname"] = dbname_override
    return params

def get_connection(dbname_override=None):
    params = get_db_params(dbname_override)
    return psycopg2.connect(**params)
