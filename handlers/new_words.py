"""
Обработчик кнопки «Новые слова».
Показывает последние добавленные слова, которые ещё не тренировались.
"""

from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Word

router = Router()


@router.message(F.text == "🆕 Новые слова")
async def show_new_words(message: Message, session: AsyncSession):
    """
    Показывает 10 последних добавленных слов со статусом 'new'.
    Красиво форматирует список с нумерацией.
    """
    user_id = message.from_user.id

    # Выбираем последние 10 новых слов
    result = await session.execute(
        select(Word)
        .where(Word.user_id == user_id, Word.status == "new")
        .order_by(Word.created_at.desc())
        .limit(10)
    )
    words = result.scalars().all()

    if not words:
        await message.answer(
            "🆕 <b>Новые слова</b>\n\n"
            "У тебя нет новых слов для изучения.\n\n"
            "📝 Нажми <b>Добавить слово</b>, чтобы пополнить словарь!\n"
            "Или все слова уже в тренировке — отлично! 🎉",
            parse_mode="HTML"
        )
        return

    # Формируем красивый список
    words_list = ""
    for i, w in enumerate(words, 1):
        words_list += (
            f"<b>{i}.</b> 🇬🇧 <b>{w.word}</b> — 🇷🇺 {w.translation}\n"
            f"    📝 <i>{w.example}</i>\n\n"
        )

    await message.answer(
        f"🆕 <b>Новые слова</b> ({len(words)} шт.)\n\n"
        f"{words_list}"
        f"💡 Нажми <b>🎯 Тренировка</b>, чтобы закрепить эти слова!",
        parse_mode="HTML"
    )
