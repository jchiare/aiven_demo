# Kafka producer / consumer to PostgreSQL app

Kafka application, using Aiven, which:
* Creates a producer 
* Generates fake testing data 
* Publishes data to a Kafka topic 
* Kafka consumer receives data and inserts into a postgres DB 

## Installation

Using requirements.txt and pip
`pip install --user --requirement requirements.txt`

Using Poetry (recommended method)
`poetry add aiven_demo`

**Note: I did not add this program to pypi for this homework**

## Running the application 

This app assumes you have an [Aiven Kafka](https://aiven.io/kafka) and [Postgres](https://aiven.io/postgresql) service created. 

1. Configure the environmental variables in the first few lines of the `Makefile` program

```
SERVICE_URI := $(or $(KAFKA_AIVEN_SERVICE_URI), "manual-input-here")
CA_PATH := $(or $(KAFKA_AIVEN_CA_PATH), "manual-input-here")
KEY_PATH := $(or $(KAFKA_AIVEN_KEY_PATH), "manual-input-here")
CERT_PATH := $(or $(KAFKA_AIVEN_CERT_PATH), "manual-input-here")
DB_URI := $(or $(POSTGRES_AIVEN_DB_URI), "manual-input-here")
```
All variables beginning with KAFKA_AIVEN are environment variables that you can set before running. Otherwise, you can set the values by replacing the `manual-input-here` text.

You can get the respective values in the **Overview** section of your aiven console for your postgres and kafka services

2. Start the Kafka consumer
`make consumer start`

3. Start the Kafka producer
`make producer start`

Optionally, the makefile comes with other functionality such as linting, checking types, and running tests

## Changing defaults

* Default is [sample_customer_profile](https://github.com/jchiare/aiven_demo/blob/main/aiven_demo/src/kafka_services/consumer.py#L27). Can also be modified with the `--topic-name` option within the CLI task. 
* TODO: add more kafka default options here

## How to run test

**No tests were created for this homework**

Ideally, I'd like to use pytest for unit tests
1. Testing main functions in the consumer, producer, and postgres setup python files

Integration tests: 
1. Sending data from producer to consumer
2. Sending data from consumer to postgres DBs

# Todo

Things that I'd like to improve in the feature
* Allow users to choose their postgres schema 
* Add testing (as noted above)
* Extend postgres DB functionality (more flexible parsing of kafka messages)
* Make other kafka defaults (like group) explicit / configurable