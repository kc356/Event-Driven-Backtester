.PHONY: help install test lint format clean run-example

help:  ## Show this help message
	@echo "Event-Driven Backtester - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

test:  ## Run tests
	pytest tests/ -v

test-watch:  ## Run tests in watch mode
	pytest tests/ -v -f

lint:  ## Run linting checks
	flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503

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

run-example:  ## Run example backtest
	python run_backtest.py --symbol SPY --start-date 2016-01-01 --end-date 2021-01-01 --strategy ETF_Forecast

run-mac:  ## Run MAC strategy backtest
	python run_backtest.py --symbol SPY --start-date 2016-01-01 --end-date 2021-01-01 --strategy MAC_Strat

run-buyhold:  ## Run Buy and Hold strategy backtest
	python run_backtest.py --symbol SPY --start-date 2016-01-01 --end-date 2021-01-01 --strategy Buy_And_Hold

all: format lint test  ## Run format, lint, and test 