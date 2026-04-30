"""
Точка входа — запуск Telegram-бота.
Инициализация БД, регистрация middleware и роутеров.
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.engine import init_db
from middlewares.db import DbSessionMiddleware
from handlers import start, add_word, new_words, training

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция — инициализация и запуск бота."""

    # Инициализируем базу данных
    logger.info("📦 Инициализация базы данных...")
    await init_db()
    logger.info("✅ База данных готова!")

    # Создаём бота с настройками по умолчанию
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Создаём диспетчер
    dp = Dispatcher()

    # Регистрируем middleware для инъекции сессии БД
    dp.update.middleware(DbSessionMiddleware())

    # Регистрируем роутеры (обработчики)
    dp.include_router(start.router)
    dp.include_router(add_word.router)
    dp.include_router(new_words.router)
    dp.include_router(training.router)

    # Запускаем бота
    logger.info("🚀 Бот запущен! Нажмите Ctrl+C для остановки.")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("👋 Бот остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
