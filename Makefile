#!/bin/bash

build:
	docker build -t statim-ai-server .

run:
	docker run --env-file .env --rm -p 5000:5000 statim-ai-server

ruff:
	poetry run ruff format .
	poetry run ruff check . --fix