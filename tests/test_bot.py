import pytest
from unittest.mock import AsyncMock, patch
from aiogram import types
from aiogram.fsm.context import FSMContext
import main
from app.database.models import User

@pytest.fixture
def message_mock():
    """Мок для объекта сообщения Telegram."""
    message = AsyncMock(spec=types.Message)
    message.from_user = AsyncMock()
    message.from_user.id = 12345
    message.from_user.full_name = "Test User"
    message.answer = AsyncMock(return_value=None)
    return message

@pytest.mark.asyncio
@patch("main.get_user_by_telegram_id")
async def test_cmd_start_user_exists(get_user_mock, message_mock):
    """Тест команды /start когда пользователь существует."""
    # Мокаем возврат пользователя из БД
    user = User(telegram_id=12345, name="Test User")
    get_user_mock.return_value = user

    # Вызываем обработчик /start
    await main.cmd_start(message_mock)

    # Проверяем что был вызов к БД с правильным ID
    get_user_mock.assert_called_once_with(12345)

    # Проверяем что отправлено правильное сообщение
    message_mock.answer.assert_called_once_with("Привет, Test User!")

@pytest.mark.asyncio
@patch("main.get_user_by_telegram_id")
async def test_cmd_start_user_not_found(get_user_mock, message_mock):
    """Тест команды /start когда пользователь не найден."""
    # Мокаем что пользователь не найден
    get_user_mock.return_value = None

    # Вызываем обработчик /start
    await main.cmd_start(message_mock)

    # Проверяем что был вызов к БД с правильным ID
    get_user_mock.assert_called_once_with(12345)

    # Проверяем что отправлено сообщение о том, что пользователь не найден
    message_mock.answer.assert_called_once_with("Пользователь не найден")

@pytest.mark.asyncio
@patch("main.get_user_by_telegram_id")
@patch("main.add_user")
async def test_cmd_addme_new_user(add_user_mock, get_user_mock, message_mock):
    """Тест команды /addme для нового пользователя."""
    # Мокаем что пользователь не найден
    get_user_mock.return_value = None

    # Мокаем добавление пользователя
    new_user = User(telegram_id=12345, name="Test User")
    add_user_mock.return_value = new_user

    # Вызываем обработчик /addme
    await main.cmd_addme(message_mock)

    # Проверяем что был вызов к БД с правильными параметрами
    get_user_mock.assert_called_once_with(12345)
    add_user_mock.assert_called_once_with(12345, "Test User")

    # Проверяем что отправлено правильное сообщение
    message_mock.answer.assert_called_once_with("Добавил тебя, Test User!")

@pytest.mark.asyncio
@patch("main.get_user_by_telegram_id")
@patch("main.add_user")
async def test_cmd_addme_existing_user(add_user_mock, get_user_mock, message_mock):
    """Тест команды /addme для существующего пользователя."""
    # Мокаем что пользователь уже существует
    user = User(telegram_id=12345, name="Test User")
    get_user_mock.return_value = user

    # Вызываем обработчик /addme
    await main.cmd_addme(message_mock)

    # Проверяем что был вызов к БД с правильным ID
    get_user_mock.assert_called_once_with(12345)

    # Проверяем что add_user не вызывался
    add_user_mock.assert_not_called()

    # Проверяем что отправлено правильное сообщение
    message_mock.answer.assert_called_once_with("Ты уже есть в базе")

@pytest.mark.asyncio
@patch("main.get_user_by_telegram_id")
async def test_echo_check(get_user_mock, message_mock):
    """Тест обработки обычного сообщения."""
    # Мокаем возврат пользователя из БД
    user = User(telegram_id=12345, name="Test User")
    get_user_mock.return_value = user

    # Вызываем обработчик сообщения
    await main.echo_check(message_mock)

    # Проверяем что был вызов к БД с правильным ID
    get_user_mock.assert_called_once_with(12345)

    # Проверяем что отправлено правильное сообщение
    message_mock.answer.assert_called_once_with("Привет, Test User!") 