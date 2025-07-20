.PHONY: help install test lint format clean docs run-example

help:  ## Show this help message
	@echo "Event-Driven Backtester - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest tests/ -v

test-watch:  ## Run tests in watch mode
	pytest tests/ -v -f

lint:  ## Run linting checks
	flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503
	mypy src/ --ignore-missing-imports

format:  ## Format code with black
	black src/ tests/ --line-length=88

format-check:  ## Check if code is formatted correctly
	black src/ tests/ --line-length=88 --check

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage

docs:  ## Build documentation
	cd docs && make html

run-example:  ## Run example backtest
	python run_backtest.py --symbol TQQQ --start-date 2016-01-01 --end-date 2021-01-01 --strategy ETF_Forecast

run-mac:  ## Run MAC strategy backtest
	python run_backtest.py --symbol TQQQ --start-date 2016-01-01 --end-date 2021-01-01 --strategy MAC_Strat

run-buyhold:  ## Run Buy and Hold strategy backtest
	python run_backtest.py --symbol TQQQ --start-date 2016-01-01 --end-date 2021-01-01 --strategy Buy_And_Hold

setup-precommit:  ## Setup pre-commit hooks
	pre-commit install

all: format lint test  ## Run format, lint, and test 