"""
Асинхронный движок SQLAlchemy + фабрика сессий.
Используем SQLite через aiosqlite для асинхронной работы.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

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
    """Создаёт все таблицы в базе данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
