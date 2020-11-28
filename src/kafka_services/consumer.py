from typing import Optional
from kafka import KafkaConsumer
import json
from typing import List

from src.postgres import connect_to_postgres, create_base_table


def start_consumer(
    service_uri: str, ca_path: str, cert_path: str, key_path: str
) -> KafkaConsumer.consumer:
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


def subscribe_consumer_by_topic(
    consumer: KafkaConsumer.consumer, topic_name: str = "sample_customer_profile"
):
    """Subscribe to Kafka topic"""
    consumer.subscribe([topic_name])


def parse_subscribed_consumer_messages(
    consumer: KafkaConsumer.consumer, pg_uri: Optional[str] = None
):
    """Add consumer messages to postgres DB"""

    db_connection = connect_to_postgres(pg_uri)
    create_base_table(db_connection)

    producter_messages = List[str]

    for message in consumer:
        producter_messages.append(message.value)

    # If there is one or more messsages
    if producter_messages:
        try:
            cursor = db_connection.cursor()
            for message in producter_messages:

                query = f"""INSERT INTO account (first_name, last_name, age, email_address)
                        VALUES ('{message['first_name']}', '{message['last_name']}', '{message['age']}', {message['email_address']});"""
                cursor.execute(query)
            cursor.close()
            db_connection.commit()
        except (Exception, psycopg2.Error) as error:
            raise RuntimeError(f"Error while inserting into PG database: {error}")
        finally:
            db_connection.close()


def close_consumer(consumer: KafkaConsumer.consumer):
    """Close consumer"""
    consumer.close()
