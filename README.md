# Telegram бот с PostgreSQL

Простой Telegram-бот на aiogram, который:
- проверяет наличие пользователя в базе по Telegram ID,
- приветствует по имени, если найден,
- добавляет нового пользователя по команде `/addme`.

## Стек
- Python 3.11
- Aiogram
- PostgreSQL + SQLAlchemy
- Alembic для миграций
- Docker
- Pytest для тестов

## Запуск локально

```bash
git clone https://github.com/username/test-task.git
cd test-task
```

```bash
python -m venv venv
source venv/bin/activate #для linux/mac
venv\Scripts\activate #на Windows
pip install -r requirements.txt
```

- создайте и заполните .env

```bash
alembic upgrade head
python main.py
```

## CI/CD
GitHub Actions запускает линтеры и тесты при каждом пуше в master, dev и при PR

## Через Docker
```bash
cp env.example .env
docker-compose up --build
```

## Тесты
```bash
pytest
```

## Структура
- **app/** — исходники
  - **database/** — модели, CRUD, подключение
  - **handlers/** — логика бота
- **alembic/** — миграции
- **main.py** — запуск бота
- **tests/** — pytest-тесты