FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Установка зависимостей системы (для psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда запуска: сначала миграции, потом приложение
CMD ["sh", "-c", "python run_migrations.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
