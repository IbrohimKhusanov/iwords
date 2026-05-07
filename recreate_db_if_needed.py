"""
Script to recreate the database from scratch and migrate data into the new schema
without IntegrityErrors.
"""

import asyncio
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from database.models import User, Word, Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///words.db"

async def recreate_and_migrate():
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    logger.info("1. Fetching existing data...")
    users_data = []
    words_data = []
    
    try:
        async with engine.begin() as conn:
            # Check if users table exists
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
            if result.scalar():
                user_rows = await conn.execute(text("SELECT * FROM users"))
                users_data = user_rows.mappings().all()
                logger.info(f"Found {len(users_data)} users.")
                
            # Check if words table exists
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='words'"))
            if result.scalar():
                word_rows = await conn.execute(text("SELECT * FROM words"))
                words_data = word_rows.mappings().all()
                logger.info(f"Found {len(words_data)} words.")
    except Exception as e:
        logger.error(f"Error reading existing data (might be missing columns): {e}")

    logger.info("2. Dropping existing tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
    logger.info("3. Recreating schema...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    logger.info("4. Restoring data...")
    async with engine.begin() as conn:
        # Restore users
        for u in users_data:
            # Map legacy fields if necessary
            kwargs = dict(u)
            if 'locale' in kwargs and 'interface_lang' not in kwargs:
                kwargs['interface_lang'] = kwargs.pop('locale')
            # Extract only fields that exist in the new User model
            valid_keys = {c.name for c in User.__table__.columns}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_keys}
            
            # Ensure defaults for required fields
            if 'interface_lang' not in filtered_kwargs:
                filtered_kwargs['interface_lang'] = 'en'
            if 'source_lang' not in filtered_kwargs:
                filtered_kwargs['source_lang'] = 'en'
            if 'target_lang' not in filtered_kwargs:
                filtered_kwargs['target_lang'] = 'ru'
            # Convert created_at to datetime if it's a string
            if 'created_at' in filtered_kwargs and isinstance(filtered_kwargs['created_at'], str):
                try:
                    filtered_kwargs['created_at'] = datetime.fromisoformat(filtered_kwargs['created_at'].replace('Z', '+00:00'))
                except ValueError:
                    try:
                        filtered_kwargs['created_at'] = datetime.strptime(filtered_kwargs['created_at'], "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass
                
            await conn.execute(User.__table__.insert().values(**filtered_kwargs))
            
        # Restore words
        for w in words_data:
            kwargs = dict(w)
            
            # Legacy mapping
            if 'word' in kwargs and 'english_word' not in kwargs:
                kwargs['english_word'] = kwargs.pop('word')
            if 'correct_count' in kwargs and 'correct_answers_count' not in kwargs:
                kwargs['correct_answers_count'] = kwargs.pop('correct_count')
                
            # Extract only fields that exist in the new Word model
            valid_keys = {c.name for c in Word.__table__.columns}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_keys}
            
            # Calculate default status and interval if they didn't exist
            if 'interval' not in filtered_kwargs:
                filtered_kwargs['interval'] = 0
            # Convert created_at and last_review to datetime if they're strings
            for date_field in ['created_at', 'last_review']:
                if date_field in filtered_kwargs and isinstance(filtered_kwargs[date_field], str):
                    try:
                        filtered_kwargs[date_field] = datetime.fromisoformat(filtered_kwargs[date_field].replace('Z', '+00:00'))
                    except ValueError:
                        try:
                            filtered_kwargs[date_field] = datetime.strptime(filtered_kwargs[date_field], "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            pass
            
            await conn.execute(Word.__table__.insert().values(**filtered_kwargs))

    logger.info("✅ Database recreated and data restored successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(recreate_and_migrate())
