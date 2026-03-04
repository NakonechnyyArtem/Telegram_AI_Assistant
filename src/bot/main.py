import asyncio
import logging
import sys
from pathlib import Path

# Добавляем корень проекта в PATH
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from src.core.config import settings
from src.core.database import db

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await db.create_pool()
    await db.init_tables()
    await message.answer("Привет! Я твой AI-ассистент. БД подключена.")

async def on_startup():
    await db.create_pool()
    await db.init_tables()
    logging.info("Бот запущен, БД инициализирована")

async def on_shutdown():
    await db.close_pool()
    await bot.session.close()
    logging.info("Бот остановлен")

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")