#!/bin/bash

VERSION := `grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3`
NAME := `grep -m 1 name pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3`
IMAGE := ${NAME}:${VERSION}
REPO := statimai

build: clean_ruff
	docker build -t ${IMAGE} .

prepare_test:
	poetry install --no-root --only=test

test:
	poetry run python tests/test_models.py

run:
	docker run --env-file .env --rm -p 5000:5000 ${IMAGE}

publish:
	docker tag ${IMAGE} ${REPO}/${IMAGE}
	docker push ${REPO}/${IMAGE}

clean_ruff:
	rm -rf .ruff_cache

ruff:
	poetry run ruff format .
	poetry run ruff check . --fix