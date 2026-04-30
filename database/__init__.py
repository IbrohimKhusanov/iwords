"""
Пакет базы данных — engine, модели, сессии.
"""

from database.engine import async_session_maker, init_db
from database.models import User, Word
