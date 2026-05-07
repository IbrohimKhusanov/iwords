"""
Handlers: /start, /settings, /help, /words, stats, language, pagination.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database.models import User, Word
from keyboards.main import main_menu_kb
from keyboards.inline import settings_kb, source_lang_kb, target_lang_kb, words_page_kb
from i18n import (
    t,
    get_flag,
    get_language_name,
    resolve_ui_locale,
    BTN_SETTINGS,
    BTN_MY_WORDS,
    BTN_RESULTS,
)

router = Router()

WORDS_PER_PAGE = 10
_BAR_SEGMENTS = 10


def _learned_bar(learned: int, total: int) -> tuple[str, float]:
    if total <= 0:
        return "⬜" * _BAR_SEGMENTS, 0.0
    pct = learned / total * 100
    filled = min(_BAR_SEGMENTS, max(0, round(learned / total * _BAR_SEGMENTS)))
    bar = "🟩" * filled + "⬜" * (_BAR_SEGMENTS - filled)
    return bar, pct


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, locale: str):
    user_id = message.from_user.id
    db_user = await session.scalar(select(User).where(User.user_id == user_id))

    if db_user:
        loc = resolve_ui_locale(db_user.target_lang)
        src = db_user.source_lang
        tgt = db_user.target_lang
    else:
        db_user = User(user_id=user_id, interface_lang="en", source_lang="en", target_lang="ru")
        session.add(db_user)
        await session.commit()
        loc = "en"
        src = "en"
        tgt = "ru"

    await message.answer(
        t(
            loc,
            "welcome",
            name=message.from_user.first_name,
            source_flag=get_flag(src),
            source_name=get_language_name(src),
            target_flag=get_flag(tgt),
            target_name=get_language_name(tgt),
        ),
        reply_markup=main_menu_kb(loc),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message, locale: str):
    await message.answer(t(locale, "help"), parse_mode="HTML")


@router.message(Command("settings"))
async def cmd_settings(message: Message, session: AsyncSession, locale: str):
    user_id = message.from_user.id
    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    source = get_language_name(db_user.source_lang if db_user else "en")
    native = get_language_name(db_user.target_lang if db_user else "ru")

    await message.answer(
        t(locale, "settings_title", source=source, native=native),
        reply_markup=settings_kb(locale),
        parse_mode="HTML",
    )


@router.message(F.text.in_(BTN_SETTINGS))
async def show_settings(message: Message, session: AsyncSession, locale: str):
    user_id = message.from_user.id
    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    source = get_language_name(db_user.source_lang if db_user else "en")
    native = get_language_name(db_user.target_lang if db_user else "ru")

    await message.answer(
        t(locale, "settings_title", source=source, native=native),
        reply_markup=settings_kb(locale),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "change_source_lang")
async def change_source_lang(callback: CallbackQuery, session: AsyncSession, locale: str):
    db_user = await session.scalar(select(User).where(User.user_id == callback.from_user.id))
    native_lang = db_user.target_lang if db_user else "ru"
    await callback.message.edit_text(
        t(locale, "choose_source_lang"),
        reply_markup=source_lang_kb(exclude_lang=native_lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_source:"))
async def set_source_lang(callback: CallbackQuery, session: AsyncSession, locale: str):
    chosen_source = callback.data.split(":")[1]
    user_id = callback.from_user.id
    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    if db_user:
        if chosen_source == db_user.target_lang:
            await callback.answer(t(locale, "choose_source_lang"), show_alert=True)
            return
        db_user.source_lang = chosen_source
        await session.commit()
    await callback.message.edit_text(
        t(locale, "source_lang_changed", lang=get_language_name(chosen_source)),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "change_target_lang")
async def change_target_lang(callback: CallbackQuery, session: AsyncSession, locale: str):
    db_user = await session.scalar(select(User).where(User.user_id == callback.from_user.id))
    source_lang = db_user.source_lang if db_user else "en"
    await callback.message.edit_text(
        t(locale, "choose_target_lang"),
        reply_markup=target_lang_kb(exclude_lang=source_lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_target:"))
async def set_target_lang(callback: CallbackQuery, session: AsyncSession, locale: str):
    chosen_target = callback.data.split(":")[1]
    user_id = callback.from_user.id

    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    if db_user:
        if chosen_target == db_user.source_lang:
            await callback.answer(t(locale, "choose_target_lang"), show_alert=True)
            return
        db_user.target_lang = chosen_target
        await session.commit()

    ui_locale = resolve_ui_locale(chosen_target)
    await callback.message.edit_text(
        t(ui_locale, "target_lang_changed", lang=get_language_name(chosen_target)),
        parse_mode="HTML",
    )
    await callback.answer()


async def _counts(session: AsyncSession, user_id: int) -> tuple[int, int, int, int]:
    total = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id)
    )
    total = int(total or 0)
    new_count = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id, Word.interval == 0)
    )
    learned_count = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id, Word.interval >= 30)
    )
    return total, int(new_count or 0), int(learned_count or 0)


@router.message(Command("stats"))
@router.message(F.text.in_(BTN_RESULTS))
async def show_my_stats(message: Message, session: AsyncSession, locale: str):
    user_id = message.from_user.id
    total, new_count, learned_count = await _counts(session, user_id)
    if not total:
        await message.answer(t(locale, "my_stats_empty"), parse_mode="HTML")
        return

    bar, pct = _learned_bar(learned_count, total)
    await message.answer(
        t(
            locale,
            "my_stats_header",
            total=total,
            new=new_count,
            learned=learned_count,
            bar=bar,
            pct=pct,
        ),
        parse_mode="HTML",
    )


def _format_words_page(
    words: list[Word],
    source_flag: str,
    flag: str,
    page: int,
    total_pages: int,
    locale: str,
) -> str:
    lines = [t(locale, "words_page_title", page=page + 1, total_pages=total_pages)]
    for w in words:
        ex = w.example or "—"
        lines.append(
            f"{source_flag} <b>{w.english_word}</b> — {flag} {w.translation}\n"
            f"📝 <i>{ex}</i>\n"
        )
    return "\n".join(lines)


@router.message(Command("words"))
@router.message(F.text.in_(BTN_MY_WORDS))
async def show_my_words(message: Message, session: AsyncSession, locale: str):
    user_id = message.from_user.id
    total = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id)
    )
    if not total:
        await message.answer(t(locale, "my_words_empty"), parse_mode="HTML")
        return

    total_pages = max(1, (total + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE)
    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    source_flag = get_flag(db_user.source_lang if db_user else "en")
    flag = get_flag(db_user.target_lang if db_user else "ru")

    result = await session.execute(
        select(Word)
        .where(Word.user_id == user_id)
        .order_by(Word.created_at.desc())
        .offset(0)
        .limit(WORDS_PER_PAGE)
    )
    words = list(result.scalars().all())
    text = _format_words_page(words, source_flag, flag, 0, total_pages, locale)
    kb = words_page_kb(locale, 0, total_pages) if total_pages > 1 else None
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("wpage:"))
async def words_page_callback(callback: CallbackQuery, session: AsyncSession, locale: str):
    user_id = callback.from_user.id
    page = int(callback.data.split(":", 1)[1])

    total = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id)
    )
    if not total:
        await callback.answer()
        return

    total_pages = max(1, (total + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE)
    page = max(0, min(page, total_pages - 1))

    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    source_flag = get_flag(db_user.source_lang if db_user else "en")
    flag = get_flag(db_user.target_lang if db_user else "ru")

    result = await session.execute(
        select(Word)
        .where(Word.user_id == user_id)
        .order_by(Word.created_at.desc())
        .offset(page * WORDS_PER_PAGE)
        .limit(WORDS_PER_PAGE)
    )
    words = list(result.scalars().all())
    text = _format_words_page(words, source_flag, flag, page, total_pages, locale)
    kb = words_page_kb(locale, page, total_pages) if total_pages > 1 else None
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()
