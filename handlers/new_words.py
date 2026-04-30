"""
Обработчик кнопки «Новые слова» / «Yangi so'zlar».
Показывает последние добавленные слова, которые ещё не тренировались.
"""

from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Word
from i18n import t, get_flag

router = Router()

# Все варианты текста кнопки
_BTN_NEW_WORDS = ["🆕 Новые слова", "🆕 Yangi so'zlar"]


@router.message(F.text.in_(_BTN_NEW_WORDS))
async def show_new_words(message: Message, session: AsyncSession, locale: str):
    """
    Показывает 10 последних добавленных слов со статусом 'new'.
    Красиво форматирует список с нумерацией.
    """
    user_id = message.from_user.id
    flag = get_flag(locale)

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
            t(locale, "new_words_empty"),
            parse_mode="HTML"
        )
        return

    # Формируем красивый список
    words_list = ""
    for i, w in enumerate(words, 1):
        words_list += (
            f"<b>{i}.</b> 🇬🇧 <b>{w.word}</b> — {flag} {w.translation}\n"
            f"    📝 <i>{w.example}</i>\n\n"
        )

    await message.answer(
        t(locale, "new_words_header", count=len(words))
        + words_list
        + t(locale, "new_words_footer"),
        parse_mode="HTML"
    )
