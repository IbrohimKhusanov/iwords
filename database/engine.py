"""
Async SQLAlchemy engine + session factory.
SQLite via aiosqlite for async operations.
"""

import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)

# Database URL — SQLite file in project root
DATABASE_URL = "sqlite+aiosqlite:///words.db"

# Async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Session factory — expire_on_commit=False is important for async
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


async def _column_exists(conn, table: str, column: str) -> bool:
    """Check if a column exists in a table."""
    result = await conn.execute(text(f"PRAGMA table_info({table})"))
    columns = [row[1] for row in result.fetchall()]
    return column in columns


async def init_db():
    """Create all tables and run migrations for existing ones."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Run idempotent migrations
    async with engine.begin() as conn:
        # --- Users table migrations ---

        # Add interface_lang column if missing
        if not await _column_exists(conn, "users", "interface_lang"):
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN interface_lang VARCHAR(5) DEFAULT 'en' NOT NULL"
            ))
            logger.info("✅ Migration: added interface_lang to users")

            # Migrate data from old 'locale' column if it exists
            if await _column_exists(conn, "users", "locale"):
                await conn.execute(text(
                    "UPDATE users SET interface_lang = locale"
                ))
                logger.info("✅ Migration: migrated locale → interface_lang")

        # Add target_lang column to users if missing
        if not await _column_exists(conn, "users", "target_lang"):
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN target_lang VARCHAR(5) DEFAULT 'ru' NOT NULL"
            ))
            logger.info("✅ Migration: added target_lang to users")

            # Set target_lang based on interface_lang
            if await _column_exists(conn, "users", "interface_lang"):
                await conn.execute(text(
                    "UPDATE users SET target_lang = CASE "
                    "WHEN interface_lang = 'uz' THEN 'uz' "
                    "ELSE 'ru' END"
                ))
                logger.info("✅ Migration: set target_lang from interface_lang")

        # --- Words table migrations ---

        # Add english_word column if missing (rename from 'word')
        if not await _column_exists(conn, "words", "english_word"):
            if await _column_exists(conn, "words", "word"):
                await conn.execute(text(
                    "ALTER TABLE words RENAME COLUMN word TO english_word"
                ))
                logger.info("✅ Migration: renamed word → english_word")
            else:
                await conn.execute(text(
                    "ALTER TABLE words ADD COLUMN english_word VARCHAR(255) DEFAULT '' NOT NULL"
                ))
                logger.info("✅ Migration: added english_word to words")

        # Add correct_answers_count column if missing
        if not await _column_exists(conn, "words", "correct_answers_count"):
            await conn.execute(text(
                "ALTER TABLE words ADD COLUMN correct_answers_count INTEGER DEFAULT 0 NOT NULL"
            ))
            logger.info("✅ Migration: added correct_answers_count to words")

            # Migrate from old correct_count if it exists
            if await _column_exists(conn, "words", "correct_count"):
                await conn.execute(text(
                    "UPDATE words SET correct_answers_count = correct_count"
                ))
                logger.info("✅ Migration: migrated correct_count → correct_answers_count")

        # Normalize NULL correct_answers_count (older rows)
        if await _column_exists(conn, "words", "correct_answers_count"):
            await conn.execute(text(
                "UPDATE words SET correct_answers_count = 0 WHERE correct_answers_count IS NULL"
            ))

        if await _column_exists(conn, "words", "status"):
            await conn.execute(text(
                "UPDATE words SET status = 'new' WHERE status IS NULL OR status = ''"
            ))
        if await _column_exists(conn, "words", "interval"):
            await conn.execute(text(
                "UPDATE words SET interval = 0 WHERE interval IS NULL"
            ))

        # Add target_lang to words if missing
        if not await _column_exists(conn, "words", "target_lang"):
            await conn.execute(text(
                "ALTER TABLE words ADD COLUMN target_lang VARCHAR(5) DEFAULT 'ru' NOT NULL"
            ))
            logger.info("✅ Migration: added target_lang to words")
