FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]