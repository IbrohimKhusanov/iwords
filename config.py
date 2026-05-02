"""
Конфигурация бота — загрузка переменных окружения.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Токен Telegram-бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Создайте файл .env и укажите токен.")



