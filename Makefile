#!/bin/bash

build:
	docker build -t statim-ai-server .

run:
	docker run --rm -p 5000:5000 statim-ai-server