from logging.config import fileConfig
import sys
import os
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Загружаем переменные окружения из .env
load_dotenv()

# Добавляем корневую директорию проекта в sys.path,
# чтобы Alembic мог импортировать модели
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем Base из ваших моделей
from app.database.models import Base

# Alembic Config object, который предоставляет доступ к .ini файлу
config = context.config

# Настройка логирования из alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Подключаем метаданные моделей для автогенерации миграций
target_metadata = Base.metadata

# Формируем строку подключения из переменных окружения
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Логируем переменные для отладки
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {'*****' if DB_PASSWORD else 'None'}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")

# Используем DATABASE_URL из окружения, если доступен
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    print(f"Используем DATABASE_URL из переменных окружения")
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

print(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL.replace(DB_PASSWORD, '*****') if DB_PASSWORD else SQLALCHEMY_DATABASE_URL}")

# Устанавливаем строку подключения в конфиг Alembic
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Конфигурируем контекст с URL без создания Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations в 'online' режиме.

    Создаём Engine и подключаемся к базе.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
