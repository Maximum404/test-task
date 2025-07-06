from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем URL из переменных окружения или используем значение по умолчанию
DATABASE_URL = os.getenv("DATABASE_URL_ASYNC")
if not DATABASE_URL:
    DATABASE_URL = "postgresql+asyncpg://postgres:12345@localhost:5432/pg_bot_db"

print(f"Подключение к БД: {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
