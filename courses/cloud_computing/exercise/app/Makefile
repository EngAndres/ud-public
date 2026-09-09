run:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8080

check-code:
	poetry run pytest tests/
	poetry run ruff format src/
	poetry run ruff check src/

docker-build:
	docker build -t my-ud-app:latest

docker-run:
	docker run -p 8000:8000 --name my-ud-app-run --env-file .env my-ud-app:latest 

alternative-deploy:
	cat /~cloud-provider/config
	cloud test-connection
	docker build -t my-ud-app:latest
	docker run -p 8000:8000 --name my-ud-app-run --env-file .env my-ud-app:latest 
	docker push
	cloud-provider computing-service deploy ....