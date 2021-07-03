
# syntax=docker/dockerfile:1

FROM python:3.6-slim-buster

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .
