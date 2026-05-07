"""
Handler: Learn New Words — /learn command + button.
Shows 5 last words with status 'new': Word — Translation — Example.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User, Word
from i18n import t, get_flag, BTN_LEARN_NEW

router = Router()


@router.message(Command("learn"))
@router.message(F.text.in_(BTN_LEARN_NEW))
async def show_learn_new(message: Message, session: AsyncSession, locale: str):
    """
    Shows 5 last added words with status 'new'.
    Format: Word — Translation — Example.
    """
    user_id = message.from_user.id

    # Get user's target lang for flag
    db_user = await session.scalar(
        select(User).where(User.user_id == user_id)
    )
    source_flag = get_flag(db_user.source_lang if db_user else "en")
    flag = get_flag(db_user.target_lang if db_user else "ru")

    # Select last 5 new words (interval = 0)
    result = await session.execute(
        select(Word)
        .where(Word.user_id == user_id, Word.interval == 0)
        .order_by(Word.created_at.desc())
        .limit(5)
    )
    words = result.scalars().all()

    if not words:
        await message.answer(
            t(locale, "learn_empty"),
            parse_mode="HTML"
        )
        return

    # Build word list
    words_list = ""
    for i, w in enumerate(words, 1):
        words_list += (
            f"<b>{i}.</b> {source_flag} <b>{w.english_word}</b> — {flag} {w.translation}\n"
            f"    📝 <i>{w.example}</i>\n\n"
        )

    await message.answer(
        t(locale, "learn_header", count=len(words))
        + words_list
        + t(locale, "learn_footer"),
        parse_mode="HTML"
    )
