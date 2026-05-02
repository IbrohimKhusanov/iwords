"""
Entry point — Telegram bot startup.
Initialize DB, register middleware and routers.
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

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def main():
    """Main function — initialize and start the bot."""

    # Initialize database
    logger.info("📦 Initializing database...")
    await init_db()
    logger.info("✅ Database ready!")

    # Create bot with default settings
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Create dispatcher
    dp = Dispatcher()

    # Register middleware for DB session injection
    dp.update.middleware(DbSessionMiddleware())

    # Register routers (handlers)
    dp.include_router(start.router)
    dp.include_router(add_word.router)
    dp.include_router(new_words.router)
    dp.include_router(training.router)

    # Start bot
    logger.info("🚀 Bot started! Press Ctrl+C to stop.")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("👋 Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
