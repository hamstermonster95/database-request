# syntax = docker/dockerfile:experimental

# Pull base image
FROM python:3.7.4

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code/

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install --upgrade pip setuptools wheel

COPY ./requirements.txt /code/

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install -r /code/requirements.txt

COPY . /code/
