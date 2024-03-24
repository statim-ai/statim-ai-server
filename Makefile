#!/bin/bash

build:
	docker build -t my-python-app .

run:
	docker run --rm -p 5000:5000 my-python-app