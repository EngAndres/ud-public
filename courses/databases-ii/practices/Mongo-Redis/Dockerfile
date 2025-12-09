FROM python:python-3.12-slim

WORKDIR app/

COPY pyproject.toml .
RUN pip install poetry
RUN poetry install

COPY src .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]