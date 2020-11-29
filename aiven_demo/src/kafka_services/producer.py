from typing import List, Any
from kafka import KafkaProducer # type: ignore
from json import dumps


# Generated from https://www.mockaroo.com/
def get_fake_data() -> List[Any]:
    data = [
        {
            "first_name": "Cindie",
            "last_name": "Anning",
            "email_address": "canning0@addthis.com",
            "age": 20,
        },
        {
            "first_name": "Carley",
            "last_name": "Gouge",
            "email_address": "cgouge1@diigo.com",
            "age": 60,
        },
        {
            "first_name": "Mari",
            "last_name": "Carvill",
            "email_address": "mcarvill2@wired.com",
            "age": 44,
        },
        {
            "first_name": "Willette",
            "last_name": "Estick",
            "email_address": "westick3@who.int",
            "age": 62,
        },
        {
            "first_name": "Boyce",
            "last_name": "Sandall",
            "email_address": "bsandall4@sfgate.com",
            "age": 36,
        },
        {
            "first_name": "Leah",
            "last_name": "Grelik",
            "email_address": "lgrelik5@adobe.com",
            "age": 30,
        },
        {
            "first_name": "Godfree",
            "last_name": "Hamsher",
            "email_address": "ghamsher6@edublogs.org",
            "age": 72,
        },
        {
            "first_name": "Yance",
            "last_name": "Bugbee",
            "email_address": "ybugbee7@narod.ru",
            "age": 22,
        },
        {
            "first_name": "Zita",
            "last_name": "Walak",
            "email_address": "zwalak8@ebay.com",
            "age": 57,
        },
        {
            "first_name": "Davie",
            "last_name": "Garmans",
            "email_address": "dgarmans9@biblegateway.com",
            "age": 53,
        },
    ]
    return data


def start_producer(service_uri: str, ca_path: str, cert_path: str, key_path: str):
    """Start the Kafka producer"""
    producer = KafkaProducer(
        bootstrap_servers=service_uri,
        security_protocol="SSL",
        ssl_cafile=ca_path,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
    )

    return producer


def send_messages_to_consumer(producer, topic_name: str = "sample_customer_profile"):
    """Send messages from Kafka producer to consumer"""
    data = get_fake_data()
    for message in data:
        print(f"Sending message from producer: {message}")
        producer.send(topic_name, dumps(message).encode("utf-8"))

    # Wait for all messages to be sent
    print(f"All producermessages sent to consumer for topic {topic_name}")
    producer.flush()
