import os

import psycopg2
from psycopg2.extensions import connection


def establish_connection() -> connection:
    connection = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_HN_DB'),
        user=os.environ.get('POSTGRES_HN_USER'),
        password=os.environ.get('POSTGRES_HN_PASSWORD'),
        host='postgres'
    )

    return connection
