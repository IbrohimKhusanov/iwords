"""
Keyboards — main menu and inline buttons.
All texts sourced from i18n module based on user locale.
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from i18n import t


def main_menu_kb(locale: str = "en") -> ReplyKeyboardMarkup:
    """Main menu with primary action buttons."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(locale, "btn_add_word")),
                KeyboardButton(text=t(locale, "btn_new_words")),
            ],
            [
                KeyboardButton(text=t(locale, "btn_training")),
                KeyboardButton(text=t(locale, "btn_progress")),
            ],
            [
                KeyboardButton(text=t(locale, "btn_settings")),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder=t(locale, "input_placeholder")
    )


def language_kb() -> InlineKeyboardMarkup:
    """Inline keyboard for language selection (3 options)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:en"),
            ],
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru"),
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang:uz"),
            ],
        ]
    )


def settings_kb(locale: str = "en") -> InlineKeyboardMarkup:
    """Inline keyboard for settings."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(locale, "settings_change_lang"),
                    callback_data="change_language"
                ),
            ],
        ]
    )


def training_kb(locale: str = "en") -> InlineKeyboardMarkup:
    """Inline keyboard during training."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(locale, "btn_next_word"), callback_data="next_word")],
            [
                InlineKeyboardButton(text=t(locale, "btn_hint"), callback_data="hint"),
                InlineKeyboardButton(text=t(locale, "btn_finish"), callback_data="finish_training"),
            ],
        ]
    )


def after_answer_kb(locale: str = "en") -> InlineKeyboardMarkup:
    """Inline keyboard after an answer in training."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(locale, "btn_next_word"), callback_data="next_word"),
                InlineKeyboardButton(text=t(locale, "btn_finish"), callback_data="finish_training"),
            ],
        ]
    )


def cancel_kb(locale: str = "en") -> InlineKeyboardMarkup:
    """Cancel button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(locale, "btn_cancel"), callback_data="cancel")],
        ]
    )
