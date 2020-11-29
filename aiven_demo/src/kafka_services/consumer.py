from typing import Optional
from kafka import KafkaConsumer
import psycopg2.Error as DBError
import json
from typing import List

from aiven_demo.src.postgres.setup import connect_to_postgres, create_base_table


def start_consumer(service_uri: str, ca_path: str, cert_path: str, key_path: str):
    """Start the Kafka consumer"""

    consumer = KafkaConsumer(
        bootstrap_servers=service_uri,
        auto_offset_reset="earliest",
        security_protocol="SSL",
        ssl_cafile=ca_path,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
        consumer_timeout_ms=10000,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="aiven-demo-group",
        client_id="kafka-python-demo",
    )

    return consumer


def subscribe_consumer_by_topic(consumer, topic_name: str = "sample_customer_profile"):
    """Subscribe to Kafka topic"""
    consumer.subscribe([topic_name])
    print("subscribed")


def parse_subscribed_consumer_messages(consumer, pg_uri: str):
    """Add consumer messages to postgres DB"""

    db_connection = connect_to_postgres(pg_uri)
    create_base_table(db_connection)

    producer_messages = List[str]

    for message in consumer:
        producer_messages.append(message.value)

    # If there is one or more messages
    if producer_messages:
        try:
            cursor = db_connection.cursor()
            for message in producer_messages:
                print(f"Received message within producer: {message}")

                query = f"""INSERT INTO account (first_name, last_name, age, email_address)
                        VALUES ('{message['first_name']}', '{message['last_name']}', '{message['age']}', {message['email_address']});"""
                cursor.execute(query)
            cursor.close()
            db_connection.commit()
        except (Exception, DBError) as error:
            raise RuntimeError(f"Error while inserting into PG database: {error}")
        finally:
            db_connection.close()


def close_consumer(consumer):
    """Close consumer"""
    consumer.close()
