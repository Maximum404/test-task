import asyncio, os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from app.database.crud import get_user_by_telegram_id, add_user

load_dotenv()

bot = Bot(os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(m: types.Message):
    user = await get_user_by_telegram_id(m.from_user.id)
    if user:
        await m.answer(f"Привет, {user.name}!")
    else:
        await m.answer("Пользователь не найден")


@dp.message(Command("addme"))
async def cmd_addme(m: types.Message):
    user = await get_user_by_telegram_id(m.from_user.id)
    if user:
        await m.answer("Ты уже есть в базе")
    else:
        user = await add_user(m.from_user.id, m.from_user.full_name)
        await m.answer(f"Добавил тебя, {user.name}!")

@dp.message()
async def echo_check(m: types.Message):
    user = await get_user_by_telegram_id(m.from_user.id)
    if user:
        await m.answer(f"Привет, {user.name}!")
    else:
        await m.answer("Пользователь не найден")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
