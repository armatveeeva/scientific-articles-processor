FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root

COPY src ./src
COPY config ./config

RUN useradd -m processor && chown -R processor /app
USER processor

CMD ["python", "-m", "articles_processor"]
