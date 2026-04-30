"""
Асинхронный движок SQLAlchemy + фабрика сессий.
Используем SQLite через aiosqlite для асинхронной работы.
"""

import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)

# URL базы данных — SQLite файл в корне проекта
DATABASE_URL = "sqlite+aiosqlite:///words.db"

# Создаём асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=False)

# Фабрика сессий — expire_on_commit=False важно для async
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""
    pass


async def init_db():
    """Создаёт все таблицы и выполняет миграции для существующих."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Автоматическая миграция: добавляем столбец target_lang в words, если его нет
    async with engine.begin() as conn:
        try:
            await conn.execute(text(
                "ALTER TABLE words ADD COLUMN target_lang VARCHAR(5) DEFAULT 'ru' NOT NULL"
            ))
            logger.info("✅ Миграция: добавлен столбец target_lang в таблицу words")
        except Exception:
            # Столбец уже существует — игнорируем
            pass
