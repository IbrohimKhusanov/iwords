"""
Training — two modes: translation → English, and sentence completion (typed answer).
SRS: correct → interval + correct_answers_count; wrong → reset interval.
"""

import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, text

from database.models import User, Word
from states.add_word import TrainingState
from keyboards.main import main_menu_kb
from keyboards.inline import train_mode_kb, training_controls_kb, after_answer_kb
from i18n import (
    t,
    get_flag,
    get_language_name,
    BTN_TRAIN,
    BTN_ADD_WORDS,
    BTN_RESULTS,
    BTN_VOCABULARY,
    BTN_SETTINGS,
    BTN_LEARN_NEW,
)

router = Router()

_MENU_TEXTS = set(
    BTN_TRAIN
    + BTN_ADD_WORDS
    + BTN_RESULTS
    + BTN_VOCABULARY
    + BTN_SETTINGS
    + BTN_LEARN_NEW
)

_WORD_DUE = or_(
    Word.interval == 0,
    Word.last_review.is_(None),
    text(
        "last_review IS NOT NULL AND last_review <= "
        "datetime('now', '-' || CAST(interval AS TEXT) || ' days')"
    ),
)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def _example_with_gap(word: Word) -> str:
    if not word.example:
        return "<b>___</b>"
    gap = word.example.replace(word.english_word, "<b>___</b>")
    if "<b>___</b>" not in gap:
        gap = re.sub(
            re.escape(word.english_word),
            "<b>___</b>",
            word.example,
            flags=re.IGNORECASE,
        )
    return gap


async def _pick_due_word(session: AsyncSession, user_id: int) -> Word | None:
    result = await session.execute(
        select(Word)
        .where(Word.user_id == user_id)
        .where(_WORD_DUE)
        .order_by(func.random())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _send_mode_picker(target, locale: str, state: FSMContext):
    await state.set_state(TrainingState.picking_mode)
    await state.update_data(score=0, total=0, mode=None, current_word_id=None)
    text = t(locale, "training_pick_mode")
    if isinstance(target, CallbackQuery):
        await target.message.answer(
            text, reply_markup=train_mode_kb(locale), parse_mode="HTML"
        )
    else:
        await target.answer(
            text, reply_markup=train_mode_kb(locale), parse_mode="HTML"
        )


async def _send_question(
    target: Message | CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user_id: int,
    locale: str,
):
    data = await state.get_data()
    mode = data.get("mode")
    score = data.get("score", 0)
    total = data.get("total", 0)

    word = await _pick_due_word(session, user_id)
    if not word:
        if total > 0:
            if score / total >= 0.8:
                comment = t(locale, "result_excellent")
            elif score / total >= 0.5:
                comment = t(locale, "result_good")
            else:
                comment = t(locale, "result_try_again")
            msg = t(locale, "training_no_more", score=score, total=total)
            if isinstance(target, CallbackQuery):
                await target.message.answer(
                    msg, reply_markup=main_menu_kb(locale), parse_mode="HTML"
                )
            else:
                await target.answer(
                    msg, reply_markup=main_menu_kb(locale), parse_mode="HTML"
                )
        else:
            msg = t(locale, "training_empty")
            if isinstance(target, CallbackQuery):
                await target.message.answer(msg, parse_mode="HTML")
            else:
                await target.answer(msg, parse_mode="HTML")
        await state.clear()
        return

    db_user = await session.scalar(select(User).where(User.user_id == user_id))
    source_lang = db_user.source_lang if db_user else "en"
    source_name = get_language_name(source_lang)
    flag = get_flag(db_user.target_lang if db_user else "ru")

    await state.update_data(current_word_id=word.id)

    if mode == "translation":
        await state.set_state(TrainingState.translation_answer)
        q = t(
            locale,
            "training_translation_ask",
            source_name=source_name,
            flag=flag,
            translation=word.translation,
        )
    else:
        await state.set_state(TrainingState.sentence_answer)
        q = t(
            locale,
            "training_sentence_ask",
            example=_example_with_gap(word),
        )

    kb = training_controls_kb(locale)
    if isinstance(target, CallbackQuery):
        await target.message.answer(q, reply_markup=kb, parse_mode="HTML")
    else:
        await target.answer(q, reply_markup=kb, parse_mode="HTML")


@router.message(Command("train"))
@router.message(F.text.in_(BTN_TRAIN))
async def start_training(
    message: Message, state: FSMContext, session: AsyncSession, locale: str
):
    await state.clear()
    await _send_mode_picker(message, locale, state)


@router.callback_query(F.data.startswith("train_mode:"))
async def pick_train_mode(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str
):
    mode = callback.data.split(":", 1)[1]
    if mode not in ("translation", "sentence"):
        await callback.answer()
        return
    await state.update_data(mode=mode, current_word_id=None)
    await _send_question(callback, state, session, callback.from_user.id, locale)
    await callback.answer()


@router.callback_query(F.data == "train_skip_word")
async def skip_word(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str
):
    data = await state.get_data()
    if not data.get("mode"):
        await callback.answer()
        return
    await _send_question(callback, state, session, callback.from_user.id, locale)
    await callback.answer()


@router.callback_query(F.data == "next_word")
async def next_word(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str
):
    data = await state.get_data()
    if not data.get("mode"):
        await callback.answer()
        return
    await _send_question(callback, state, session, callback.from_user.id, locale)
    await callback.answer()


@router.callback_query(F.data == "hint")
async def show_hint(callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str):
    data = await state.get_data()
    word_id = data.get("current_word_id")
    if not word_id:
        await callback.answer(t(locale, "hint_no_word"))
        return

    word = await session.get(Word, word_id)
    if not word:
        await callback.answer(t(locale, "hint_not_found"))
        return

    if word.example:
        await callback.answer(
            t(locale, "hint_example_sentence", example=word.example),
            show_alert=True,
        )
        return

    w = word.english_word
    if len(w) <= 2:
        hint = w
    else:
        hint = f"{w[0]}{'_' * (len(w) - 2)}{w[-1]}"
    await callback.answer(
        t(locale, "hint_text", hint=hint, length=len(w)),
        show_alert=True,
    )


def _left_until_learned(word: Word) -> int:
    cur = word.interval
    if cur >= 30:
        return 0
    milestones = [1, 3, 7, 14, 30]
    return sum(1 for m in milestones if m > cur)


async def _grade_answer(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    locale: str,
    *,
    expected: str,
):
    raw = message.text or ""
    if raw in _MENU_TEXTS:
        await state.clear()
        await message.answer(
            t(locale, "training_cancelled_menu"),
            reply_markup=main_menu_kb(locale),
            parse_mode="HTML",
        )
        return

    data = await state.get_data()
    word_id = data.get("current_word_id")
    score = data.get("score", 0)
    total = data.get("total", 0)

    if not word_id:
        return

    word = await session.get(Word, word_id)
    if not word:
        await state.clear()
        await message.answer(t(locale, "training_empty"), parse_mode="HTML")
        return

    db_user = await session.scalar(select(User).where(User.user_id == message.from_user.id))
    source_flag = get_flag(db_user.source_lang if db_user else "en")
    flag = get_flag(db_user.target_lang if db_user else "ru")

    ok = _norm(raw) == _norm(expected)
    total += 1

    if ok:
        score += 1
        word.record_correct()
        await session.commit()

        status_text = ""
        if word.interval >= 30:
            status_text = t(locale, "training_learned")
        else:
            left = _left_until_learned(word)
            if left > 0:
                status_text = t(locale, "training_progress", left=left)

        await message.answer(
            t(
                locale,
                "training_correct",
                source_flag=source_flag,
                word=word.english_word,
                flag=flag,
                translation=word.translation,
                example=word.example or "",
                score=score,
                total=total,
                status_text=status_text,
            ),
            reply_markup=after_answer_kb(locale),
            parse_mode="HTML",
        )
    else:
        word.record_wrong()
        await session.commit()
        await message.answer(
            t(
                locale,
                "training_incorrect",
                source_flag=source_flag,
                word=word.english_word,
                flag=flag,
                translation=word.translation,
                example=word.example or "",
                score=score,
                total=total,
            ),
            reply_markup=after_answer_kb(locale),
            parse_mode="HTML",
        )

    await state.update_data(score=score, total=total)


@router.message(TrainingState.translation_answer, F.text)
async def answer_translation(
    message: Message, state: FSMContext, session: AsyncSession, locale: str
):
    data = await state.get_data()
    word_id = data.get("current_word_id")
    if not word_id:
        return
    word = await session.get(Word, word_id)
    if not word:
        return
    await _grade_answer(
        message, state, session, locale, expected=word.english_word
    )


@router.message(TrainingState.sentence_answer, F.text)
async def answer_sentence(
    message: Message, state: FSMContext, session: AsyncSession, locale: str
):
    data = await state.get_data()
    word_id = data.get("current_word_id")
    if not word_id:
        return
    word = await session.get(Word, word_id)
    if not word:
        return
    await _grade_answer(
        message, state, session, locale, expected=word.english_word
    )


@router.callback_query(F.data == "finish_training")
async def finish_training(callback: CallbackQuery, state: FSMContext, locale: str):
    data = await state.get_data()
    score = data.get("score", 0)
    total = data.get("total", 0)

    if total == 0:
        comment = t(locale, "result_no_answers")
    elif score / total >= 0.8:
        comment = t(locale, "result_excellent")
    elif score / total >= 0.5:
        comment = t(locale, "result_good")
    else:
        comment = t(locale, "result_try_again")

    await callback.message.answer(
        t(locale, "training_finished", score=score, total=total, comment=comment),
        reply_markup=main_menu_kb(locale),
        parse_mode="HTML",
    )
    await state.clear()
    await callback.answer()
