from aiven_demo.src.kafka_services.consumer import (
    start_consumer,
    subscribe_consumer_by_topic,
    parse_subscribed_consumer_messages,
    close_consumer,
)
from aiven_demo.src.kafka_services.producer import (
    start_producer,
    send_messages_to_consumer,
)

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Run a Kafka consumer or producer")
    parser.add_argument(
        "--service-uri", help="Service URI in the form host:port", required=True
    )
    parser.add_argument(
        "--ca-path", help="Path to project CA certificate", required=True
    )
    parser.add_argument(
        "--key-path",
        help="Path to the Kafka Access Key (obtained from Aiven Console)",
        required=True,
    )
    parser.add_argument(
        "--cert-path",
        help="Path to the Kafka Certificate Key (obtained from Aiven Console)",
        required=True,
    )
    parser.add_argument("--postgres-db-uri", help="Optional postgresDB URI")
    parser.add_argument("--topic-name", help="Optional postgresDB URI", default=None)
    parser.add_argument(
        "--consumer",
        action="store_true",
        default=False,
        help="Run Kafka consumer example",
    )
    parser.add_argument(
        "--producer",
        action="store_true",
        default=False,
        help="Run Kafka producer example",
    )
    args = parser.parse_args()
    validate_args(args)

    kwargs = {
        k: v
        for k, v in vars(args).items()
        if k not in ("producer", "consumer", "postgres_db_uri") and v is not None
    }
    if args.producer:
        producer = start_producer(**kwargs)
        send_messages_to_consumer(producer)

    elif args.consumer:
        consumer = start_consumer(**kwargs)
        subscribe_consumer_by_topic(consumer)
        parse_subscribed_consumer_messages(consumer, vars(args)["postgres_db_uri"])
        close_consumer(consumer)


def validate_args(args) -> None:
    for path_option in ("ca_path", "key_path", "cert_path"):
        path = getattr(args, path_option)
        if not os.path.isfile(path):
            fail(
                f"Failed to open --{path_option.replace('_', '-')} at path: {path}.\n"
                f"You can retrieve these details from Overview tab in the Aiven Console"
            )
    if args.producer and args.consumer:
        fail("--producer and --consumer are mutually exclusive")
    elif not args.producer and not args.consumer:
        fail("--producer or --consumer are required")


def fail(message: str) -> exit:
    print(message, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
