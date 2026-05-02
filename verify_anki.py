import asyncio
from datetime import datetime, timedelta
from database.models import User, Word
from database.engine import init_db, engine, async_session_maker

async def test_anki():
    # Setup fresh tables
    async with engine.begin() as conn:
        from database.engine import Base
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session_maker() as session:
        # Create user
        u = User(user_id=999)
        session.add(u)
        
        # Create word
        w = Word(user_id=999, english_word="hello", translation="привет", status="new")
        session.add(w)
        await session.commit()
        
        # Initial state
        assert w.interval == 0
        assert w.status == "new"
        
        # Record correct 1
        w.record_correct()
        assert w.interval == 1
        assert w.status == "learning"
        assert w.last_review is not None
        
        # Record correct 2
        w.record_correct()
        assert w.interval == 3
        
        # Record wrong
        w.record_wrong()
        assert w.interval == 0
        assert w.status == "new"
        
        # Fast forward
        w.record_correct() # -> 1
        w.record_correct() # -> 3
        w.record_correct() # -> 7
        w.record_correct() # -> 14
        w.record_correct() # -> 30
        assert w.interval == 30
        assert w.status == "learned"
        
        print("✅ SRS Logic OK!")

if __name__ == "__main__":
    asyncio.run(test_anki())
