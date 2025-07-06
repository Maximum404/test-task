FROM python:3.11-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Устанавливаем переменные окружения по умолчанию
ENV BOT_TOKEN=""
ENV DATABASE_URL="postgresql+asyncpg://postgres:12345@postgres:5432/pg_bot_db"

# Команда запуска
CMD ["python", "main.py"]