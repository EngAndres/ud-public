SHELL := /bin/bash -c

hello:
	@echo "Hello, UD!"

format-code:
	@echo "======= Formatting code..."
	black .

lint-code:
	@echo "======= Linting code..."
	find . -name "*.py" | xargs pylint

test-code:
	@echo "======= Testing code..."
	poetry run pytest -v

pre-commit:
	@echo "======= Running pre-commit checks..."
	black .
	find . -name "*.py" | xargs pylint
	poetry run pytest -v