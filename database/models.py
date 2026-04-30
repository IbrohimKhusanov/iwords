"""
Модели базы данных — таблица слов пользователя.
"""

import json
from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import BigInteger, String, Text, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from database.engine import Base


class Word(Base):
    """
    Модель слова в словаре пользователя.

    Поля:
        id — уникальный ID
        user_id — Telegram user_id
        word — английское слово
        translation — перевод на русский
        example — пример предложения
        status — статус: 'new', 'learning', 'learned'
        correct_count — общее количество правильных ответов
        correct_dates — JSON-список дат правильных ответов (для интервального повторения)
        created_at — дата добавления
    """

    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    word: Mapped[str] = mapped_column(String(255), nullable=False)
    translation: Mapped[str] = mapped_column(String(255), nullable=False)
    example: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="new")
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    correct_dates: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="[]")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def get_correct_dates(self) -> List[str]:
        """Возвращает список дат правильных ответов."""
        if not self.correct_dates:
            return []
        return json.loads(self.correct_dates)

    def add_correct_date(self, dt: date) -> None:
        """
        Добавляет дату правильного ответа.
        Если набрано ≥ 3 уникальных дней — помечает слово как 'learned'.
        """
        dates = self.get_correct_dates()
        date_str = dt.isoformat()

        # Добавляем дату, если её ещё нет
        if date_str not in dates:
            dates.append(date_str)

        self.correct_dates = json.dumps(dates)
        self.correct_count += 1

        # Интервальное повторение: 3+ уникальных дня → выучено
        if len(dates) >= 3:
            self.status = "learned"
        elif len(dates) >= 1:
            self.status = "learning"

    def __repr__(self) -> str:
        return f"<Word(id={self.id}, word='{self.word}', status='{self.status}')>"
