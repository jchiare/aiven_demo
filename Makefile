SERVICE_URI := $(or $(KAFKA_AIVEN_SERVICE_URI), "manual-input-here")
CA_PATH := $(or $(KAFKA_AIVEN_CA_PATH), "manual-input-here")
KEY_PATH := $(or $(KAFKA_AIVEN_KEY_PATH), "manual-input-here")
CERT_PATH := $(or $(KAFKA_AIVEN_CERT_PATH), "manual-input-here")
DB_URI := $(or $(POSTGRES_AIVEN_DB_URI), "manual-input-here")

lint:
	poetry run black .
	poetry run flake8

check:
	poetry run mypy aiven_demo

test:
	poetry run pytest

install:
	poetry install

build:
	poetry run build

consumer start:
	poetry run python3 aiven_demo/src/main.py --service-uri ${SERVICE_URI} --ca-path ${CA_PATH} --key-path ${KEY_PATH} --cert-path ${CERT_PATH} --postgres-db-uri ${DB_URI} --consumer

producer start: 
	poetry run python3 aiven_demo/src/main.py --service-uri ${SERVICE_URI} --ca-path ${CA_PATH} --key-path ${KEY_PATH} --cert-path ${CERT_PATH} --producer