SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:
BUILDOS=$(shell uname -s | tr '[:upper:]' '[:lower:]')


.PHONY: help
help:
	echo "❓ Use \`make <target>'"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: install ## Install dependencies
install:
	uv sync

.PHONY: host ## Run the host CLI
host:
	uv run host/jiki.py

.PHONY: lint ## Run linter
lint:
	ruff check .

.PHONY: fix ## Run linter and fix
fix:
	ruff check . --fix
	ruff format .
