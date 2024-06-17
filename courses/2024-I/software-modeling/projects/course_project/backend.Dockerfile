# syntax=docker/dockerfile:1.2

FROM python:3.11-slim-buster

WORKDIR /app

COPY course_project/ .

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]