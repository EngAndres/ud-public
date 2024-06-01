FROM --platform=arm64 python:3.11

WORKDIR /app/

COPY course_project/ .

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080"]