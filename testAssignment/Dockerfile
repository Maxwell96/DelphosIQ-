# syntax=docker/dockerfile:1

# Pull base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY . /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/