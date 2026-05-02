import asyncio
import logging
import sys
import os
from aiohttp import web # Убедись, что сделал pip install aiohttp

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.engine import init_db
from middlewares.db import DbSessionMiddleware
from handlers import start, add_word, new_words, training

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)

# --- ТЕХНИЧЕСКИЙ БЛОК ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Bot is Live!")

async def start_render_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Привязываемся к порту 10000 (стандарт Render)
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🌐 [Render] Web server started on port {port}")

# --- ОСНОВНАЯ ФУНКЦИЯ ---
async def main():
    # 1. Сначала запускаем веб-сервер для порта
    await start_render_server()

    # 2. Инициализация БД
    logger.info("📦 Initializing database...")
    await init_db()
    logger.info("✅ Database ready!")

    # 3. Настройка бота
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware())

    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(add_word.router)
    dp.include_router(new_words.router)
    dp.include_router(training.router)

    logger.info("🚀 Bot started!")
    try:
        # ПЕРЕД ЭТИМ ВЫКЛЮЧИ БОТА НА КОМПЬЮТЕРЕ!
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
