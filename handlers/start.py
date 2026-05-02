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
from keyboards.inline import settings_kb, target_lang_kb, words_page_kb
from i18n import t, get_flag, BTN_SETTINGS, BTN_MY_WORDS, BTN_RESULTS, TARGET_LANG_DISPLAY

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
        loc = db_user.interface_lang
    else:
        db_user = User(user_id=user_id, interface_lang="en", target_lang="ru")
        session.add(db_user)
        await session.commit()
        loc = "en"

    await message.answer(
        t(loc, "welcome", name=message.from_user.first_name),
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
    target = TARGET_LANG_DISPLAY.get(db_user.target_lang, "Русский") if db_user else "Русский"

    await message.answer(
        t(locale, "settings_title", target=target),
        reply_markup=settings_kb(locale),
        parse_mode="HTML",
    )


@router.message(F.text.in_(BTN_SETTINGS))
async def show_settings(message: Message, session: AsyncSession, locale: str):
    user_id = message.from_user.id
    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    target = TARGET_LANG_DISPLAY.get(db_user.target_lang, "Русский") if db_user else "Русский"

    await message.answer(
        t(locale, "settings_title", target=target),
        reply_markup=settings_kb(locale),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "change_target_lang")
async def change_target_lang(callback: CallbackQuery, locale: str):
    await callback.message.edit_text(
        t(locale, "choose_target_lang"),
        reply_markup=target_lang_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_target:"))
async def set_target_lang(callback: CallbackQuery, session: AsyncSession, locale: str):
    chosen_target = callback.data.split(":")[1]
    user_id = callback.from_user.id

    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    if db_user:
        db_user.target_lang = chosen_target
        await session.commit()

    lang_name = TARGET_LANG_DISPLAY.get(chosen_target, chosen_target)
    await callback.message.edit_text(
        t(locale, "target_lang_changed", lang=lang_name),
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
    flag: str,
    page: int,
    total_pages: int,
    locale: str,
) -> str:
    lines = [t(locale, "words_page_title", page=page + 1, total_pages=total_pages)]
    for w in words:
        ex = w.example or "—"
        lines.append(
            f"🇬🇧 <b>{w.english_word}</b> — {flag} {w.translation}\n"
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
    flag = get_flag(db_user.target_lang if db_user else "ru")

    result = await session.execute(
        select(Word)
        .where(Word.user_id == user_id)
        .order_by(Word.created_at.desc())
        .offset(0)
        .limit(WORDS_PER_PAGE)
    )
    words = list(result.scalars().all())
    text = _format_words_page(words, flag, 0, total_pages, locale)
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
    flag = get_flag(db_user.target_lang if db_user else "ru")

    result = await session.execute(
        select(Word)
        .where(Word.user_id == user_id)
        .order_by(Word.created_at.desc())
        .offset(page * WORDS_PER_PAGE)
        .limit(WORDS_PER_PAGE)
    )
    words = list(result.scalars().all())
    text = _format_words_page(words, flag, page, total_pages, locale)
    kb = words_page_kb(locale, page, total_pages) if total_pages > 1 else None
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()
