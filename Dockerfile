FROM python:3.14-slim

# Установка системных зависимостей для psycopg
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN pip install uv

# Установка рабочей директории
WORKDIR /

# Копирование файлов с зависимостями из корня проекта
COPY pyproject.toml uv.lock ./

# Установка зависимостей через uv
RUN uv sync --frozen

# Добавляем путь к виртуальному окружению в PATH
ENV PATH="/.venv/bin:$PATH"

# Устанавливаем Python путь для импортов
ENV PYTHONPATH="${PYTHONPATH}:/"

# Создаем директорию для приложения
WORKDIR /app

# Копирование остальных файлов проекта
COPY ./app .

# Копирование alembic директории (если она находится на том же уровне, что и app)
COPY ./alembic /alembic
COPY ./alembic.ini /alembic.ini

WORKDIR /

# Команда по умолчанию (будет переопределена в docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
