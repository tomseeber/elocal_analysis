SHELL := /bin/bash

.PHONY: help deps test lint

help:
	@echo "Makefile commands: deps, test, lint"

deps:
	pip install -r requirements.txt

test:
	pytest -q

lint:
	flake8 src tests || true
