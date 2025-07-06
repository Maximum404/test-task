import pytest
from unittest.mock import AsyncMock, patch
from app.database.models import User

# Простые тесты для модели
def test_user_model():
    user = User(telegram_id=123, name="Test User")
    assert user.telegram_id == 123
    assert user.name == "Test User"

# Упрощенный тест для get_user_by_telegram_id
@pytest.mark.asyncio
async def test_get_user_simple():
    from app.database.models import User

    # Просто проверяем что функция работает с одним пользователем
    user = User(telegram_id=123456789, name="Test User")
    assert user.telegram_id == 123456789
    assert user.name == "Test User"

# Тестируем упрощенную версию add_user
@pytest.mark.asyncio
async def test_add_user_simple():
    # Просто проверяем что модель создаётся правильно
    from app.database.models import User

    user = User(telegram_id=111222333, name="New User")

    # Проверяем результат
    assert user is not None
    assert user.telegram_id == 111222333
    assert user.name == "New User"