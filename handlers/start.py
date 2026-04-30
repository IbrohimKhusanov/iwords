"""
Обработчик команды /start и кнопки «Мой прогресс».
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database.models import Word
from keyboards.main import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработчик команды /start.
    Приветствие + главное меню.
    """
    await message.answer(
        f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
        "🇬🇧 Я — бот для изучения английских слов.\n\n"
        "📝 <b>Добавь слово</b> — и я переведу его автоматически\n"
        "🆕 <b>Новые слова</b> — посмотри недавно добавленные\n"
        "🎯 <b>Тренировка</b> — проверь свои знания\n"
        "📊 <b>Мой прогресс</b> — твоя статистика\n\n"
        "🚀 Давай начнём!",
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )


@router.message(F.text == "📊 Мой прогресс")
async def show_progress(message: Message, session: AsyncSession):
    """
    Показывает статистику пользователя:
    - всего слов
    - новых / в процессе / выученных
    """
    user_id = message.from_user.id

    # Общее количество слов
    total = await session.scalar(
        select(func.count(Word.id)).where(Word.user_id == user_id)
    )

    # По статусам
    new_count = await session.scalar(
        select(func.count(Word.id)).where(
            Word.user_id == user_id, Word.status == "new"
        )
    )
    learning_count = await session.scalar(
        select(func.count(Word.id)).where(
            Word.user_id == user_id, Word.status == "learning"
        )
    )
    learned_count = await session.scalar(
        select(func.count(Word.id)).where(
            Word.user_id == user_id, Word.status == "learned"
        )
    )

    # Формируем красивый отчёт
    if total == 0:
        await message.answer(
            "📊 <b>Твой прогресс</b>\n\n"
            "У тебя пока нет слов в словаре.\n"
            "Нажми <b>📝 Добавить слово</b>, чтобы начать! 🚀",
            parse_mode="HTML"
        )
        return

    # Прогресс-бар
    if total > 0:
        progress = learned_count / total * 100
    else:
        progress = 0

    bar_filled = int(progress / 10)
    bar_empty = 10 - bar_filled
    progress_bar = "🟩" * bar_filled + "⬜" * bar_empty

    await message.answer(
        f"📊 <b>Твой прогресс</b>\n\n"
        f"📚 Всего слов: <b>{total}</b>\n\n"
        f"🆕 Новые: <b>{new_count}</b>\n"
        f"📖 Изучаются: <b>{learning_count}</b>\n"
        f"✅ Выучены: <b>{learned_count}</b>\n\n"
        f"Прогресс: {progress_bar} {progress:.0f}%\n\n"
        f"{'🔥 Отличная работа! Продолжай!' if progress >= 50 else '💪 Так держать! Продолжай тренироваться!'}",
        parse_mode="HTML"
    )
