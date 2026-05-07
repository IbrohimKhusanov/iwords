"""
Handler: add word(s). Button + /add command.
Batch lists run in a background task; reports are sent in chunks of 10–15 words.
"""

import re
import asyncio

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User, Word
from database.engine import async_session_maker
from states.add_word import AddWordState
from keyboards.main import main_menu_kb
from keyboards.inline import cancel_kb
from services.translator import translate_word
from i18n import t, get_flag, BTN_ADD_WORDS

router = Router()

_SPLIT = re.compile(r"[,;\n]+")
_MAX_WORDS = 150
_THROTTLE_EVERY = 5
_THROTTLE_DELAY = 0.5
_COMMIT_BATCH = 25
_PROGRESS_EVERY = 5
_MSG_LIMIT = 4000
_CHUNK_SIZE = 12


def _parse(text: str) -> list[str]:
    return [p.strip().lower() for p in _SPLIT.split(text) if p.strip()]


def _valid(w: str) -> bool:
    return bool(w) and all(c.isalpha() or c.isspace() or c == "-" for c in w)


def _progress(done: int, total: int, locale: str) -> str:
    pct = int(done / total * 100) if total else 0
    bar = "▓" * (pct // 10) + "░" * (10 - pct // 10)
    return t(locale, "progress_bar", bar=bar, pct=pct, done=done, total=total)


@router.message(Command("add"))
@router.message(F.text.in_(BTN_ADD_WORDS))
async def start_add_word(message: Message, state: FSMContext, locale: str):
    await state.set_state(AddWordState.waiting_for_word)
    await message.answer(
        t(locale, "add_word_prompt", max_words=_MAX_WORDS),
        parse_mode="HTML",
        reply_markup=cancel_kb(locale),
    )


@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext, locale: str):
    await state.clear()
    await callback.message.answer(
        t(locale, "cancel_action"),
        reply_markup=main_menu_kb(locale),
    )
    await callback.answer()


@router.message(AddWordState.waiting_for_word)
async def process_word(message: Message, state: FSMContext, session: AsyncSession, locale: str):
    words = _parse(message.text.strip())
    if not words:
        await message.answer(t(locale, "word_not_recognized"), parse_mode="HTML")
        return
    if len(words) > _MAX_WORDS:
        await message.answer(
            t(locale, "too_many_words", max_words=_MAX_WORDS, count=len(words)),
            parse_mode="HTML",
        )
        return

    if len(words) == 1:
        await _single(message, state, session, words[0], locale)
    else:
        await state.clear()
        await message.answer(
            t(locale, "batch_started", count=len(words)),
            parse_mode="HTML",
        )
        asyncio.create_task(
            _batch_background(message.bot, message.chat.id, message.from_user.id, words, locale)
        )


async def _get_lang_pair(session: AsyncSession, user_id: int) -> tuple[str, str]:
    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    if not db_user:
        return "en", "ru"
    return db_user.source_lang, db_user.target_lang


async def _single(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    word_in: str,
    locale: str,
):
    if not _valid(word_in):
        await message.answer(t(locale, "invalid_word"), parse_mode="HTML")
        return

    uid = message.from_user.id
    src, tgt = await _get_lang_pair(session, uid)
    source_flag = get_flag(src)
    flag = get_flag(tgt)

    existing = await session.scalar(
        select(Word).where(Word.user_id == uid, Word.english_word == word_in)
    )
    if existing:
        await message.answer(
            t(
                locale,
                "word_exists",
                word=word_in,
                flag=flag,
                translation=existing.translation,
                example=existing.example or "—",
            ),
            parse_mode="HTML",
        )
        return

    wait_msg = await message.answer(t(locale, "translating"))
    result = translate_word(word_in, source_lang=src, target_lang=tgt)

    session.add(
        Word(
            user_id=uid,
            english_word=result["word"],
            translation=result["translation"],
            example=result["example"],
            status="new",
            correct_answers_count=0,
            interval=0,
        )
    )
    await session.commit()
    await wait_msg.delete()
    await state.clear()

    await message.answer(
        t(
            locale,
            "word_added",
            source_flag=source_flag,
            word=result["word"],
            flag=flag,
            translation=result["translation"],
            example=result["example"],
        ),
        reply_markup=main_menu_kb(locale),
        parse_mode="HTML",
    )


async def _batch_background(bot: Bot, chat_id: int, user_id: int, words: list[str], locale: str):
    async with async_session_maker() as session:
        src, tgt = await _get_lang_pair(session, user_id)
        source_flag = get_flag(src)
        flag = get_flag(tgt)
        total = len(words)
        prog_msg = await bot.send_message(chat_id, _progress(0, total, locale), parse_mode="HTML")

        added: list[dict] = []
        dup: list[str] = []
        bad: list[str] = []
        uncommitted = 0

        for i, w in enumerate(words, 1):
            if not _valid(w):
                bad.append(w)
                continue
            ex = await session.scalar(
                select(Word).where(Word.user_id == user_id, Word.english_word == w)
            )
            if ex:
                dup.append(w)
                continue

            r = translate_word(w, source_lang=src, target_lang=tgt)
            session.add(
                Word(
                    user_id=user_id,
                    english_word=r["word"],
                    translation=r["translation"],
                    example=r["example"],
                    status="new",
                    correct_answers_count=0,
                    interval=0,
                )
            )
            added.append(r)
            uncommitted += 1

            if uncommitted >= _COMMIT_BATCH:
                await session.commit()
                uncommitted = 0
            if i % _THROTTLE_EVERY == 0:
                await asyncio.sleep(_THROTTLE_DELAY)
            if i % _PROGRESS_EVERY == 0 or i == total:
                try:
                    await prog_msg.edit_text(_progress(i, total, locale), parse_mode="HTML")
                except Exception:
                    pass

        if uncommitted > 0:
            await session.commit()
        try:
            await prog_msg.delete()
        except Exception:
            pass

        await _send_batch_reports(bot, chat_id, added, dup, bad, locale, source_flag, flag)


async def _send_batch_reports(
    bot: Bot,
    chat_id: int,
    added: list[dict],
    dup: list[str],
    bad: list[str],
    locale: str,
    source_flag: str,
    flag: str,
):
    header = (
        t(locale, "batch_added", count=len(added))
        if added
        else t(locale, "batch_none_added")
    )

    footer_parts = []
    if dup:
        preview = ", ".join(w.capitalize() for w in dup[:20])
        sfx = f" +{len(dup) - 20}…" if len(dup) > 20 else ""
        footer_parts.append(
            t(locale, "batch_duplicates", count=len(dup), list=preview + sfx)
        )
    if bad:
        preview = ", ".join(bad[:10])
        sfx = f" +{len(bad) - 10}…" if len(bad) > 10 else ""
        footer_parts.append(t(locale, "batch_invalid", count=len(bad), list=preview + sfx))
    footer_parts.append(t(locale, "batch_continue"))
    footer = "\n".join(footer_parts)

    if not added:
        await bot.send_message(
            chat_id,
            header + footer,
            reply_markup=main_menu_kb(locale),
            parse_mode="HTML",
        )
        return

    chunks = [added[i : i + _CHUNK_SIZE] for i in range(0, len(added), _CHUNK_SIZE)]
    for ci, chunk in enumerate(chunks):
        parts: list[str] = []
        if ci == 0:
            parts.append(header)
        off = ci * _CHUNK_SIZE
        for j, r in enumerate(chunk, off + 1):
            parts.append(
                f"  {j}. {source_flag} <b>{r['word']}</b> — {flag} {r['translation']}\n"
                f"      📝 <i>{r['example']}</i>"
            )
        is_last = ci == len(chunks) - 1
        if is_last:
            parts.append("")
            parts.append(footer)
        txt = "\n".join(parts)
        if len(txt) > _MSG_LIMIT:
            txt = txt[: _MSG_LIMIT - 20] + "\n\n<i>…truncated</i>"
        await bot.send_message(
            chat_id,
            txt,
            reply_markup=main_menu_kb(locale) if is_last else None,
            parse_mode="HTML",
        )
        if not is_last:
            await asyncio.sleep(0.35)
