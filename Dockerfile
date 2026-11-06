FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Устанавливаем системные зависимости для chemdataextractor и dawg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Добавляем chemdataextractor только для продакшена в Docker
RUN poetry install --only main,docker --no-root

# Устанавливаем основные зависимости
RUN poetry install --only main --no-root

# Копируем исходный код
COPY src ./src
COPY config ./config

# Создаем непривилегированного пользователя для безопасности (production best practice)
RUN useradd -m processor && chown -R processor /app
USER processor

CMD ["python", "-m", "articles_processor"]
