FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y vim

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .
