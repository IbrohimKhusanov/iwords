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

router = Router()


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


def _format_question(word: Word) -> str:
    """
    Формирует вопрос для тренировки.
    Случайно выбирает один из двух режимов:
    1. Показать перевод → угадать слово
    2. Показать пример с пропуском → угадать слово
    """
    mode = random.choice(["translation", "example"])

    if mode == "translation" or not word.example:
        # Режим: перевод → слово
        status_emoji = {"new": "🆕", "learning": "📖", "learned": "✅"}.get(word.status, "")
        return (
            f"🎯 <b>Тренировка</b> {status_emoji}\n\n"
            f"🇷🇺 Перевод: <b>{word.translation}</b>\n\n"
            f"❓ Напиши английское слово:"
        )
    else:
        # Режим: пример с пропуском → слово
        # Заменяем слово в примере на пропуск
        example_with_gap = word.example.replace(
            word.word, "<b>___</b>"
        )
        return (
            f"🎯 <b>Тренировка</b>\n\n"
            f"📝 Заполни пропуск:\n"
            f"<i>{example_with_gap}</i>\n\n"
            f"🇷🇺 Подсказка: {word.translation}\n\n"
            f"❓ Напиши слово:"
        )


@router.message(F.text == "🎯 Тренировка")
async def start_training(message: Message, state: FSMContext, session: AsyncSession):
    """Начало тренировки — выбираем случайное слово."""
    user_id = message.from_user.id

    word = await _get_training_word(session, user_id)

    if not word:
        await message.answer(
            "🎯 <b>Тренировка</b>\n\n"
            "У тебя пока нет слов для тренировки.\n"
            "Сначала добавь несколько слов через <b>📝 Добавить слово</b>! 🚀",
            parse_mode="HTML"
        )
        return

    # Сохраняем текущее слово в FSM
    await state.set_state(TrainingState.in_training)
    await state.update_data(current_word_id=word.id, score=0, total=0)

    question = _format_question(word)
    await message.answer(question, reply_markup=training_kb(), parse_mode="HTML")


@router.message(TrainingState.in_training)
async def check_answer(message: Message, state: FSMContext, session: AsyncSession):
    """
    Проверка ответа пользователя.
    Сравнивает введённое слово с правильным (case-insensitive).
    """
    data = await state.get_data()
    word_id = data.get("current_word_id")
    score = data.get("score", 0)
    total = data.get("total", 0)

    if not word_id:
        await message.answer("⚠️ Ошибка тренировки. Начни заново.", reply_markup=main_menu_kb())
        await state.clear()
        return

    # Получаем слово из БД
    word = await session.get(Word, word_id)
    if not word:
        await message.answer("⚠️ Слово не найдено. Начни тренировку заново.", reply_markup=main_menu_kb())
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
            status_text = "\n\n🏆 Слово помечено как <b>выученное</b>!"
        elif word.status == "learning":
            dates_left = 3 - len(word.get_correct_dates())
            status_text = f"\n\n📈 Осталось {dates_left} дн. до статуса «выучено»"

        await message.answer(
            f"✅ <b>Правильно!</b> 🎉\n\n"
            f"🇬🇧 <b>{word.word}</b> — 🇷🇺 {word.translation}\n"
            f"📝 <i>{word.example}</i>\n\n"
            f"📊 Счёт: <b>{score}/{total}</b>"
            f"{status_text}",
            reply_markup=after_answer_kb(),
            parse_mode="HTML"
        )
    else:
        # Неправильный ответ
        await message.answer(
            f"❌ <b>Неверно!</b>\n\n"
            f"Твой ответ: <s>{user_answer}</s>\n"
            f"Правильно: 🇬🇧 <b>{word.word}</b>\n"
            f"🇷🇺 {word.translation}\n"
            f"📝 <i>{word.example}</i>\n\n"
            f"📊 Счёт: <b>{score}/{total}</b>\n\n"
            f"💡 Запомни и попробуй в следующий раз!",
            reply_markup=after_answer_kb(),
            parse_mode="HTML"
        )

    # Обновляем данные FSM
    await state.update_data(score=score, total=total)


@router.callback_query(F.data == "next_word")
async def next_word(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Следующее слово в тренировке."""
    user_id = callback.from_user.id

    word = await _get_training_word(session, user_id)

    if not word:
        data = await state.get_data()
        score = data.get("score", 0)
        total = data.get("total", 0)
        await callback.message.answer(
            f"🏁 <b>Тренировка завершена!</b>\n\n"
            f"📊 Результат: <b>{score}/{total}</b>\n"
            f"Больше нет слов для тренировки. Добавь новые! 🚀",
            reply_markup=main_menu_kb(),
            parse_mode="HTML"
        )
        await state.clear()
        await callback.answer()
        return

    # Обновляем текущее слово
    await state.update_data(current_word_id=word.id)

    question = _format_question(word)
    await callback.message.answer(question, reply_markup=training_kb(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "hint")
async def show_hint(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Показать подсказку — первую и последнюю букву слова."""
    data = await state.get_data()
    word_id = data.get("current_word_id")

    if not word_id:
        await callback.answer("⚠️ Нет текущего слова")
        return

    word = await session.get(Word, word_id)
    if not word:
        await callback.answer("⚠️ Слово не найдено")
        return

    # Подсказка: первая буква + длина + последняя буква
    w = word.word
    if len(w) <= 2:
        hint = w
    else:
        hint = f"{w[0]}{'_' * (len(w) - 2)}{w[-1]}"

    await callback.answer(f"💡 Подсказка: {hint} ({len(w)} букв)", show_alert=True)


@router.callback_query(F.data == "finish_training")
async def finish_training(callback: CallbackQuery, state: FSMContext):
    """Завершение тренировки — показываем итоги."""
    data = await state.get_data()
    score = data.get("score", 0)
    total = data.get("total", 0)

    # Определяем комментарий к результату
    if total == 0:
        comment = "Попробуй в следующий раз! 💪"
    elif score / total >= 0.8:
        comment = "🔥 Великолепно! Ты настоящий мастер!"
    elif score / total >= 0.5:
        comment = "👍 Хороший результат! Продолжай тренироваться!"
    else:
        comment = "💪 Не сдавайся! Повторение — мать учения!"

    await callback.message.answer(
        f"🏁 <b>Тренировка завершена!</b>\n\n"
        f"📊 Результат: <b>{score}/{total}</b>\n\n"
        f"{comment}",
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )
    await state.clear()
    await callback.answer()
