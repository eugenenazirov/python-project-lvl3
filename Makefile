install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

test-logging:
	poetry run pytest -o log_cli=true -o log_cli_level=INFO

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

build:
	poetry build

page-loader:
	poetry run page-loader

.PHONY: install test lint selfcheck check build page-loader
