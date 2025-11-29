.PHONY: install run test lint format clean help

PYTHON := python3
PIP := pip

help:
	@echo "Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make run        Run the FastAPI server"
	@echo "  make test       Run tests with pytest"
	@echo "  make lint       Run linting (flake8, mypy)"
	@echo "  make format     Format code (black, isort)"
	@echo "  make clean      Remove build artifacts and cache"

install:
	$(PIP) install -r requirements.txt
	$(PIP) install black isort flake8 mypy pytest pytest-cov httpx

run:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	PYTHONPATH=. pytest

lint:
	flake8 backend tests
	mypy backend tests

format:
	black backend tests
	isort backend tests

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
