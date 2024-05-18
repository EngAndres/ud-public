format-code: 
	black .

lint-code:
	find /backend -name "*.py" | xargs pylint

smell-code:
	black .
	pytest -v
	find . -name "*.py" | xargs pylint