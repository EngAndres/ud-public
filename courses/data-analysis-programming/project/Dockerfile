FROM python:3.11-slim

WORKDIR app/

COPY pyproject.toml .
RUN pip install poetry
RUN poetry install

COPY src/ .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]