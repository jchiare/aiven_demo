lint:
	poetry run black .
	poetry run flake8

check:
	poetry run mypy .

test:
	poetry run pytest

install:
	poetry install