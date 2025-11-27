# execute this python version
FROM python:3.13-slim

# prevent some python execution files using environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install linux packages
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# setup app
WORKDIR /app
COPY pyproject.toml poetry.lock
RUN pip install poetry && poetry install
# RUN poetry install --without dev -> for prof

COPY src/ .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]