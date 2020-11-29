import os
import psycopg2
from typing import Optional


def get_postgres_uri() -> Optional[str]:
    """
    Return postgres URI using POSTGRES_URI env variable

    Returns:
        Optional - string - uri of the postgres env
    """
    if not os.environ.get("POSTGRES_URI"):
        raise RuntimeError("The POSTGRES_URI config variable is not set.")
    return os.environ.get("POSTGRES_URI")


def connect_to_postgres(
    user_postgres_uri: Optional[str],
) -> Optional[psycopg2.connection]:
    """
    Connect to postgres DB

    Arguments:
        user_postgres_uri -- URI of the postgres db given from user

    Returns:
        Optional - psycopg2.connection - connection to Postgres DB
    """
    postgres_uri = user_postgres_uri if user_postgres_uri else get_postgres_uri()

    try:
        connection = psycopg2.connect(postgres_uri)
        return connection

    except (Exception, psycopg2.Error) as error:
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

    except (Exception, psycopg2.Error) as error:
        raise RuntimeError(f"Error creating database table: {error}")
