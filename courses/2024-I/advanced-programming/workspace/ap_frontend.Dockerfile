# syntax=docker/dockerfile:1.2

# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /frontend

# Install dependencies
COPY requirements_frontend.txt /frontend/
RUN pip install --no-cache-dir -r requirements_frontend.txt

# Copy project
COPY ./frontend /frontend/

# Expose port
EXPOSE 80

# Run the application:
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]