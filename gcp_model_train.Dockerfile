FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY football_match_predictor/model ./football_match_predictor/model
COPY football_match_predictor/util ./football_match_predictor/util

ENTRYPOINT ["poetry", "run", "python", "-m", "football_match_predictor.model.gcp_model_train"]
