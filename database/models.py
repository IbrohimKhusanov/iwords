"""
Database models — User and Word tables.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String, Text, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from database.engine import Base


class User(Base):
    """
    User model.

    Fields:
        id — primary key
        user_id — Telegram user_id (unique)
        interface_lang — UI language ('en', 'ru', 'uz'), default 'en'
        source_lang — language user learns, default 'en'
        target_lang — translation/native language, default 'ru'
        created_at — registration date
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, index=True)
    interface_lang: Mapped[str] = mapped_column(String(5), default="en", nullable=False)
    source_lang: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    target_lang: Mapped[str] = mapped_column(String(10), default="ru", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, user_id={self.user_id}, "
            f"interface_lang='{self.interface_lang}', source_lang='{self.source_lang}', "
            f"target_lang='{self.target_lang}')>"
        )


class Word(Base):
    """
    Word model — user's vocabulary entry with Anki SRS support.

    Fields:
        id — primary key
        user_id — Telegram user_id
        english_word — the English word
        translation — translation in target language
        example — example sentence in English
        correct_answers_count — legacy field, keeping for compatibility
        status — word status: 'new', 'learning', or 'learned'
        created_at — date added
        last_review — date of last review (SRS)
        interval — current interval in days (SRS)
    """

    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    english_word: Mapped[str] = mapped_column(String(255), nullable=False)
    translation: Mapped[str] = mapped_column(String(255), nullable=False)
    example: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    correct_answers_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )

    # Status dynamically updated based on interval
    status: Mapped[str] = mapped_column(String(20), default="new", nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    
    # Anki SRS fields
    last_review: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    interval: Mapped[int] = mapped_column(Integer, default=0)

    def _update_status(self):
        if self.interval == 0:
            self.status = "new"
        elif 0 < self.interval < 30:
            self.status = "learning"
        else:
            self.status = "learned"

    def record_correct(self):
        """
        Record a correct answer. Increases interval: 0 -> 1 -> 3 -> 7 -> 14 -> 30.
        """
        self.correct_answers_count = int(self.correct_answers_count or 0) + 1
        if self.interval == 0:
            self.interval = 1
        elif self.interval == 1:
            self.interval = 3
        elif self.interval == 3:
            self.interval = 7
        elif self.interval == 7:
            self.interval = 14
        else:
            self.interval = 30
            
        self.last_review = datetime.utcnow()
        self._update_status()

    def record_wrong(self):
        """
        Record a wrong answer. Resets interval to 0.
        """
        self.interval = 0
        self.last_review = datetime.utcnow()
        self._update_status()

    def __repr__(self) -> str:
        return (
            f"<Word(id={self.id}, english_word='{self.english_word}', "
            f"interval={self.interval}, status='{self.status}')>"
        )
