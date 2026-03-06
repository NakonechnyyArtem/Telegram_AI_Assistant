import asyncio
import logging
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from aiogram import Bot, Dispatcher
from src.core.config import settings
from src.core.database import db

from src.handlers.start import router as start_router
from src.handlers.help import router as help_router
from src.handlers.settings import router as settings_router
from src.handlers.stats import router as stats_router

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(help_router)
dp.include_router(settings_router)
dp.include_router(stats_router)

async def on_startup():
    await db.create_pool()
    await db.init_tables()
    logging.info(" Бот запущен, БД инициализирована")

async def on_shutdown():
    await db.close_pool()
    await bot.session.close()
    logging.info(" Бот остановлен")

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")