FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY football_match_predictor/config ./football_match_predictor/config
COPY football_match_predictor/experiments ./football_match_predictor/experiments
COPY football_match_predictor/util ./football_match_predictor/util

ENTRYPOINT ["poetry", "run", "python", "-m", "football_match_predictor.experiments.cross_validation"]
