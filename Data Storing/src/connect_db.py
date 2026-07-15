import psycopg2

db_params = {
    "dbname": "ck3_db",
    "user": "postgres",
    "password": "andracantik",
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**db_params)
