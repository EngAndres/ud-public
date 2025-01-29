FROM python=3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8247"]