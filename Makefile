#!/bin/bash

build: clean_ruff
	docker build -t statim-ai-server .

run:
	docker run --env-file .env --rm -p 5000:5000 statim-ai-server

clean_ruff:
	rm -rf .ruff_cache

ruff:
	poetry run ruff format .
	poetry run ruff check . --fix