import os
from psycopg2 import DBconnect, DBerror
from typing import Optional

def connect_to_postgres(
    postgres_uri: str,
) -> Optional[DBconnect]:
    """
    Connect to postgres DB

    Arguments:
        postgres_uri -- URI of the postgres db

    Returns:
        Optional - DBconnect - connection to Postgres DB
    """

    try:
        connection = DBconnect(postgres_uri)
        return connection

    except (Exception, DBerror) as error:
        raise RuntimeError(f"Error attempting to connect to Postgres DB: {error}")


def create_base_table(pg_conn) -> None:
    """
    Create table for postgres db if it doesn't exist
    """
    try:
        cursor = pg_conn.cursor()

        cursor.execute(
            """
                        CREATE TABLE IF NOT EXISTS customer_profile(
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR (40) NOT NULL,
                        last_name VARCHAR (40) NOT NULL,
                        age INTEGER NOT NULL,
                        email_address VARCHAR (255) NOT NULL,
                        created_at timestamp default NOW()
                        );
                        """
        )
        cursor.close()
        pg_conn.commit()

    except (Exception, DBerror) as error:
        raise RuntimeError(f"Error creating database table: {error}")
