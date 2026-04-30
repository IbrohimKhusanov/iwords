"""
Handler: add word(s). Button + /add command.
FSM: waiting for input → parse → translate → save.
"""

import re
import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Word
from states.add_word import AddWordState
from keyboards.main import main_menu_kb, cancel_kb
from services.translator import translate_word
from i18n import t, get_flag, get_target_lang, BTN_ADD_WORD

router = Router()

_SPLIT = re.compile(r"[,;\n]+")
_MAX_WORDS = 150
_THROTTLE_EVERY = 5
_THROTTLE_DELAY = 0.5
_COMMIT_BATCH = 25
_PROGRESS_EVERY = 5
_MSG_LIMIT = 4000
_CHUNK_SIZE = 30


def _parse(text: str) -> list[str]:
    return [p.strip().lower() for p in _SPLIT.split(text) if p.strip()]


def _valid(w: str) -> bool:
    return bool(w) and all(c.isalpha() or c.isspace() or c == "-" for c in w)


def _progress(done: int, total: int, locale: str) -> str:
    pct = int(done / total * 100) if total else 0
    bar = "▓" * (pct // 10) + "░" * (10 - pct // 10)
    return t(locale, "progress_bar", bar=bar, pct=pct, done=done, total=total)


@router.message(Command("add"))
@router.message(F.text.in_(BTN_ADD_WORD))
async def start_add_word(message: Message, state: FSMContext, locale: str):
    await state.set_state(AddWordState.waiting_for_word)
    await message.answer(
        t(locale, "add_word_prompt", max_words=_MAX_WORDS),
        parse_mode="HTML", reply_markup=cancel_kb(locale)
    )


@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext, locale: str):
    await state.clear()
    await callback.message.answer(
        t(locale, "cancel_action"), reply_markup=main_menu_kb(locale)
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
            parse_mode="HTML"
        )
        return

    if len(words) == 1:
        await _single(message, state, session, words[0], locale)
    else:
        await _batch(message, state, session, words, locale)


async def _single(message: Message, state: FSMContext, session: AsyncSession,
                   word_in: str, locale: str):
    if not _valid(word_in):
        await message.answer(t(locale, "invalid_word"), parse_mode="HTML")
        return

    uid = message.from_user.id
    flag = get_flag(locale)
    tgt = get_target_lang(locale)

    existing = await session.scalar(
        select(Word).where(Word.user_id == uid, Word.word == word_in)
    )
    if existing:
        await message.answer(
            t(locale, "word_exists", word=word_in, flag=flag,
              translation=existing.translation, example=existing.example),
            parse_mode="HTML"
        )
        return

    wait_msg = await message.answer(t(locale, "translating"))
    result = translate_word(word_in, target_lang=tgt)

    session.add(Word(
        user_id=uid, word=result["word"], translation=result["translation"],
        example=result["example"], target_lang=tgt, status="new"
    ))
    await session.commit()
    await wait_msg.delete()
    await state.clear()

    await message.answer(
        t(locale, "word_added", word=result["word"], flag=flag,
          translation=result["translation"], example=result["example"]),
        reply_markup=main_menu_kb(locale), parse_mode="HTML"
    )


async def _batch(message: Message, state: FSMContext, session: AsyncSession,
                  words: list[str], locale: str):
    uid = message.from_user.id
    total = len(words)
    flag = get_flag(locale)
    tgt = get_target_lang(locale)

    prog_msg = await message.answer(_progress(0, total, locale), parse_mode="HTML")

    added, dup, bad = [], [], []
    uncommitted = 0

    for i, w in enumerate(words, 1):
        if not _valid(w):
            bad.append(w); continue
        ex = await session.scalar(select(Word).where(Word.user_id == uid, Word.word == w))
        if ex:
            dup.append(w); continue

        r = translate_word(w, target_lang=tgt)
        session.add(Word(
            user_id=uid, word=r["word"], translation=r["translation"],
            example=r["example"], target_lang=tgt, status="new"
        ))
        added.append(r)
        uncommitted += 1

        if uncommitted >= _COMMIT_BATCH:
            await session.commit(); uncommitted = 0
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

    await state.clear()
    await _send_result(message, added, dup, bad, locale, flag)


async def _send_result(message: Message, added, dup, bad, locale, flag):
    header = t(locale, "batch_added", count=len(added)) if added else t(locale, "batch_none_added")

    footer_parts = []
    if dup:
        preview = ", ".join(w.capitalize() for w in dup[:20])
        sfx = f" +{len(dup)-20}…" if len(dup) > 20 else ""
        footer_parts.append(t(locale, "batch_duplicates", count=len(dup), list=preview + sfx))
    if bad:
        preview = ", ".join(bad[:10])
        sfx = f" +{len(bad)-10}…" if len(bad) > 10 else ""
        footer_parts.append(t(locale, "batch_invalid", count=len(bad), list=preview + sfx))
    footer_parts.append(t(locale, "batch_continue"))
    footer = "\n".join(footer_parts)

    if not added:
        await message.answer(header + footer, reply_markup=main_menu_kb(locale), parse_mode="HTML")
        return

    chunks = [added[i:i+_CHUNK_SIZE] for i in range(0, len(added), _CHUNK_SIZE)]
    for ci, chunk in enumerate(chunks):
        parts = []
        if ci == 0:
            parts.append(header)
        off = ci * _CHUNK_SIZE
        for j, r in enumerate(chunk, off + 1):
            parts.append(f"  {j}. 🇬🇧 <b>{r['word']}</b> — {flag} {r['translation']}\n      📝 <i>{r['example']}</i>")
        is_last = ci == len(chunks) - 1
        if is_last:
            parts.append("")
            parts.append(footer)
        txt = "\n".join(parts)
        if len(txt) > _MSG_LIMIT:
            txt = txt[:_MSG_LIMIT - 20] + "\n\n<i>…truncated</i>"
        await message.answer(txt, reply_markup=main_menu_kb(locale) if is_last else None, parse_mode="HTML")
        if not is_last:
            await asyncio.sleep(0.3)
