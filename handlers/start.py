"""
Handlers: /start, /settings, /help, progress button, language selection.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database.models import User, Word
from keyboards.main import main_menu_kb, language_kb, settings_kb
from i18n import t, BTN_PROGRESS, BTN_SETTINGS

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, locale: str):
    """First launch → language picker; returning user → welcome."""
    user_id = message.from_user.id
    db_user = await session.scalar(select(User).where(User.user_id == user_id))

    if db_user:
        loc = db_user.locale
        await message.answer(
            t(loc, "welcome", name=message.from_user.first_name),
            reply_markup=main_menu_kb(loc), parse_mode="HTML"
        )
    else:
        await message.answer(
            t("en", "choose_language"),
            reply_markup=language_kb(), parse_mode="HTML"
        )


@router.message(Command("help"))
async def cmd_help(message: Message, locale: str):
    """/help — show available commands."""
    await message.answer(t(locale, "help"), parse_mode="HTML")


@router.message(Command("settings"))
async def cmd_settings(message: Message, locale: str):
    """/settings — open settings menu."""
    await message.answer(
        t(locale, "settings_title"),
        reply_markup=settings_kb(locale), parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("set_lang:"))
async def set_language(callback: CallbackQuery, session: AsyncSession):
    """Handle language choice — create/update user, refresh menu."""
    chosen_locale = callback.data.split(":")[1]
    user_id = callback.from_user.id

    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    if db_user:
        db_user.locale = chosen_locale
    else:
        db_user = User(user_id=user_id, locale=chosen_locale)
        session.add(db_user)
    await session.commit()

    await callback.message.edit_text(
        t(chosen_locale, "lang_changed"), parse_mode="HTML"
    )
    await callback.message.answer(
        t(chosen_locale, "welcome", name=callback.from_user.first_name),
        reply_markup=main_menu_kb(chosen_locale), parse_mode="HTML"
    )
    await callback.answer()


@router.message(F.text.in_(BTN_SETTINGS))
async def show_settings(message: Message, locale: str):
    """Settings button handler."""
    await message.answer(
        t(locale, "settings_title"),
        reply_markup=settings_kb(locale), parse_mode="HTML"
    )


@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery, locale: str):
    """Show language picker from settings."""
    await callback.message.edit_text(
        t(locale, "choose_language"),
        reply_markup=language_kb(), parse_mode="HTML"
    )
    await callback.answer()


@router.message(F.text.in_(BTN_PROGRESS))
async def show_progress(message: Message, session: AsyncSession, locale: str):
    """Show user progress statistics."""
    user_id = message.from_user.id

    total = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id)
    )
    if total == 0:
        await message.answer(t(locale, "progress_empty"), parse_mode="HTML")
        return

    new_count = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id, Word.status == "new")
    )
    learning_count = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id, Word.status == "learning")
    )
    learned_count = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id, Word.status == "learned")
    )

    progress = learned_count / total * 100 if total > 0 else 0
    bar_filled = int(progress / 10)
    progress_bar = "🟩" * bar_filled + "⬜" * (10 - bar_filled)
    comment = t(locale, "progress_great") if progress >= 50 else t(locale, "progress_keep")

    await message.answer(
        t(locale, "progress_stats",
          total=total, new=new_count, learning=learning_count,
          learned=learned_count, bar=progress_bar, pct=progress, comment=comment),
        parse_mode="HTML"
    )
