install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

lint:
	poetry run flake8 page-loader

selfcheck:
	poetry check

check: selfcheck test lint

build:
	poetry build

page-loader:
	poetry run page-loader

.PHONY: install test lint selfcheck check build page-loader
