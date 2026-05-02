"""
Reply keyboard — main menu. Inline keyboards live in keyboards.inline.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from i18n import t


def main_menu_kb(locale: str = "en") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(locale, "btn_train")),
                KeyboardButton(text=t(locale, "btn_add_words")),
            ],
            [
                KeyboardButton(text=t(locale, "btn_results")),
                KeyboardButton(text=t(locale, "btn_vocabulary")),
            ],
            [KeyboardButton(text=t(locale, "btn_settings"))],
        ],
        resize_keyboard=True,
        input_field_placeholder=t(locale, "input_placeholder"),
    )
