"""
Inline keyboards — settings, training, vocabulary pagination.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from i18n import t


def language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:en")],
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru"),
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang:uz"),
            ],
        ]
    )


def target_lang_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_target:ru"),
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_target:uz"),
            ],
        ]
    )


def settings_kb(locale: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(locale, "settings_change_target"),
                    callback_data="change_target_lang",
                ),
            ],
        ]
    )


def train_mode_kb(locale: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(locale, "btn_mode_translation"),
                    callback_data="train_mode:translation",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t(locale, "btn_mode_sentence"),
                    callback_data="train_mode:sentence",
                ),
            ],
        ]
    )


def training_controls_kb(locale: str = "en") -> InlineKeyboardMarkup:
    """During a question: Next, Hint, Finish."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(locale, "btn_next_word"), callback_data="train_skip_word"),
                InlineKeyboardButton(text=t(locale, "btn_hint"), callback_data="hint"),
            ],
            [
                InlineKeyboardButton(text=t(locale, "btn_finish"), callback_data="finish_training"),
            ],
        ]
    )


def after_answer_kb(locale: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(locale, "btn_next_word"), callback_data="next_word"),
                InlineKeyboardButton(text=t(locale, "btn_finish"), callback_data="finish_training"),
            ],
        ]
    )


def words_page_kb(locale: str, page: int, total_pages: int) -> InlineKeyboardMarkup:
    row = []
    if page > 0:
        row.append(
            InlineKeyboardButton(text="⬅️ " + t(locale, "btn_prev_page"), callback_data=f"wpage:{page - 1}")
        )
    if page < total_pages - 1:
        row.append(
            InlineKeyboardButton(text=t(locale, "btn_next_page") + " ➡️", callback_data=f"wpage:{page + 1}")
        )
    return InlineKeyboardMarkup(inline_keyboard=[row] if row else [])


def cancel_kb(locale: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(locale, "btn_cancel"), callback_data="cancel")],
        ]
    )
