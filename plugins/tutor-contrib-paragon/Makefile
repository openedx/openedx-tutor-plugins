.DEFAULT_GOAL := help
.PHONY: docs
SRC_DIRS = ./tutorparagon

# Warning: These checks are not necessarily run on every PR.
test: test-lint test-types test-format  # Run some static checks.

test-format: ## Run code formatting tests
	ruff format --check --diff $(SRC_DIRS)

test-lint: ## Run code linting tests
	ruff check ${SRC_DIRS}

test-types: ## Run type checks.
	mypy --exclude=templates --ignore-missing-imports --implicit-reexport --strict ${SRC_DIRS}

format: ## Format code automatically
	ruff format ${SRC_DIRS}

fix-lint: ## Fix lint errors automatically
	ruff check --fix ${SRC_DIRS}

unittest: ## Run code tests cases
	pytest tests --ignore=tests/integration

integration-test: ## Run integration tests cases
	pytest tests/integration --order-scope=module

dev-requirements: ## Install dev requirements
	pip install -e .[dev]

run-tests: test unittest integration-test  # Run all tests: static analysis, unit tests, and integration tests

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
