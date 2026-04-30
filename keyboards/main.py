"""
Клавиатуры бота — главное меню и inline-кнопки.
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def main_menu_kb() -> ReplyKeyboardMarkup:
    """Главное меню бота с основными кнопками."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Добавить слово"),
                KeyboardButton(text="🆕 Новые слова"),
            ],
            [
                KeyboardButton(text="🎯 Тренировка"),
                KeyboardButton(text="📊 Мой прогресс"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard


def training_kb() -> InlineKeyboardMarkup:
    """Inline-клавиатура во время тренировки."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏭ Следующее слово", callback_data="next_word"),
            ],
            [
                InlineKeyboardButton(text="💡 Подсказка", callback_data="hint"),
                InlineKeyboardButton(text="🏁 Закончить", callback_data="finish_training"),
            ],
        ]
    )
    return keyboard


def after_answer_kb() -> InlineKeyboardMarkup:
    """Inline-клавиатура после ответа на тренировке."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏭ Следующее слово", callback_data="next_word"),
                InlineKeyboardButton(text="🏁 Закончить", callback_data="finish_training"),
            ],
        ]
    )
    return keyboard


def cancel_kb() -> InlineKeyboardMarkup:
    """Кнопка отмены."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"),
            ],
        ]
    )
    return keyboard
