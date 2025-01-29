FROM --platform=arm64 python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY /condor/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]