"""
Обработчик тренировки — основной режим обучения.
Случайная выборка слов, проверка ответов, интервальное повторение.
"""

import random
from datetime import date

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database.models import Word
from states.add_word import TrainingState
from keyboards.main import main_menu_kb, training_kb, after_answer_kb
from i18n import t, get_flag

router = Router()

# Все варианты текста кнопки
_BTN_TRAINING = ["🎯 Тренировка", "🎯 Mashq qilish"]


async def _get_training_word(session: AsyncSession, user_id: int) -> Word | None:
    """
    Выбирает случайное слово для тренировки.
    Приоритет: new > learning > learned (реже).
    """
    # Сначала пробуем взять новое или изучаемое слово
    result = await session.execute(
        select(Word)
        .where(
            Word.user_id == user_id,
            Word.status.in_(["new", "learning"])
        )
        .order_by(func.random())
        .limit(1)
    )
    word = result.scalar_one_or_none()

    if word:
        return word

    # Если нет новых/изучаемых — берём выученное (для повторения)
    result = await session.execute(
        select(Word)
        .where(Word.user_id == user_id)
        .order_by(func.random())
        .limit(1)
    )
    return result.scalar_one_or_none()


def _format_question(word: Word, locale: str) -> str:
    """
    Формирует вопрос для тренировки.
    Случайно выбирает один из двух режимов:
    1. Показать перевод → угадать слово
    2. Показать пример с пропуском → угадать слово
    """
    mode = random.choice(["translation", "example"])
    flag = get_flag(locale)

    if mode == "translation" or not word.example:
        # Режим: перевод → слово
        status_emoji = {"new": "🆕", "learning": "📖", "learned": "✅"}.get(word.status, "")
        return t(locale, "training_q_translation",
                 status_emoji=status_emoji, flag=flag,
                 translation=word.translation)
    else:
        # Режим: пример с пропуском → слово
        example_with_gap = word.example.replace(word.word, "<b>___</b>")
        return t(locale, "training_q_example",
                 example=example_with_gap, flag=flag,
                 translation=word.translation)


@router.message(F.text.in_(_BTN_TRAINING))
async def start_training(message: Message, state: FSMContext, session: AsyncSession, locale: str):
    """Начало тренировки — выбираем случайное слово."""
    user_id = message.from_user.id

    word = await _get_training_word(session, user_id)

    if not word:
        await message.answer(
            t(locale, "training_empty"),
            parse_mode="HTML"
        )
        return

    # Сохраняем текущее слово в FSM
    await state.set_state(TrainingState.in_training)
    await state.update_data(current_word_id=word.id, score=0, total=0)

    question = _format_question(word, locale)
    await message.answer(question, reply_markup=training_kb(locale), parse_mode="HTML")


@router.message(TrainingState.in_training)
async def check_answer(message: Message, state: FSMContext, session: AsyncSession, locale: str):
    """
    Проверка ответа пользователя.
    Сравнивает введённое слово с правильным (case-insensitive).
    """
    data = await state.get_data()
    word_id = data.get("current_word_id")
    score = data.get("score", 0)
    total = data.get("total", 0)
    flag = get_flag(locale)

    if not word_id:
        await message.answer(
            t(locale, "training_error"),
            reply_markup=main_menu_kb(locale)
        )
        await state.clear()
        return

    # Получаем слово из БД
    word = await session.get(Word, word_id)
    if not word:
        await message.answer(
            t(locale, "training_word_missing"),
            reply_markup=main_menu_kb(locale)
        )
        await state.clear()
        return

    user_answer = message.text.strip().lower()
    correct_answer = word.word.strip().lower()
    total += 1

    if user_answer == correct_answer:
        # Правильный ответ! 🎉
        score += 1

        # Обновляем интервальное повторение
        word.add_correct_date(date.today())
        await session.commit()

        status_text = ""
        if word.status == "learned":
            status_text = t(locale, "training_learned")
        elif word.status == "learning":
            dates_left = 3 - len(word.get_correct_dates())
            status_text = t(locale, "training_days_left", days=dates_left)

        await message.answer(
            t(locale, "training_correct",
              word=word.word, flag=flag,
              translation=word.translation,
              example=word.example,
              score=score, total=total,
              status_text=status_text),
            reply_markup=after_answer_kb(locale),
            parse_mode="HTML"
        )
    else:
        # Неправильный ответ
        await message.answer(
            t(locale, "training_incorrect",
              answer=user_answer, word=word.word,
              flag=flag, translation=word.translation,
              example=word.example,
              score=score, total=total),
            reply_markup=after_answer_kb(locale),
            parse_mode="HTML"
        )

    # Обновляем данные FSM
    await state.update_data(score=score, total=total)


@router.callback_query(F.data == "next_word")
async def next_word(callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str):
    """Следующее слово в тренировке."""
    user_id = callback.from_user.id

    word = await _get_training_word(session, user_id)

    if not word:
        data = await state.get_data()
        score = data.get("score", 0)
        total = data.get("total", 0)
        await callback.message.answer(
            t(locale, "training_no_more", score=score, total=total),
            reply_markup=main_menu_kb(locale),
            parse_mode="HTML"
        )
        await state.clear()
        await callback.answer()
        return

    # Обновляем текущее слово
    await state.update_data(current_word_id=word.id)

    question = _format_question(word, locale)
    await callback.message.answer(question, reply_markup=training_kb(locale), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "hint")
async def show_hint(callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str):
    """Показать подсказку — первую и последнюю букву слова."""
    data = await state.get_data()
    word_id = data.get("current_word_id")

    if not word_id:
        await callback.answer(t(locale, "hint_no_word"))
        return

    word = await session.get(Word, word_id)
    if not word:
        await callback.answer(t(locale, "hint_not_found"))
        return

    # Подсказка: первая буква + длина + последняя буква
    w = word.word
    if len(w) <= 2:
        hint = w
    else:
        hint = f"{w[0]}{'_' * (len(w) - 2)}{w[-1]}"

    await callback.answer(
        t(locale, "hint_text", hint=hint, length=len(w)),
        show_alert=True
    )


@router.callback_query(F.data == "finish_training")
async def finish_training(callback: CallbackQuery, state: FSMContext, locale: str):
    """Завершение тренировки — показываем итоги."""
    data = await state.get_data()
    score = data.get("score", 0)
    total = data.get("total", 0)

    # Определяем комментарий к результату
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
        parse_mode="HTML"
    )
    await state.clear()
    await callback.answer()
