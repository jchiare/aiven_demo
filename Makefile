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