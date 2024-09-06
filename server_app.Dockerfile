FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY football_match_predictor/model ./football_match_predictor/model
COPY football_match_predictor/server ./football_match_predictor/server
COPY football_match_predictor/util ./football_match_predictor/util

ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "300", "football_match_predictor.server.app:app"]

