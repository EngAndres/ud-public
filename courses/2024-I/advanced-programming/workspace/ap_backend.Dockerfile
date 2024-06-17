# syntax=docker/dockerfile:1.2

# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /backend

# Copy the requirements.txt file into the container at /app
COPY requirements_backend.txt /backend/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements_backend.txt

# Copy the current directory contents into the container at /app
COPY ./backend /backend/

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the command to start uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]