"""
Сервис перевода — deep-translator (Google).
Переводит слова и генерирует контекстные примеры на английском.
"""

import random

from deep_translator import GoogleTranslator


EXAMPLE_TEMPLATES = [
    "I always try to {word} when I have free time.",
    "She asked me to {word}, and I agreed immediately.",
    "Learning to {word} is an important life skill.",
    "He couldn't {word} because he was too tired.",
    "We should {word} more often to stay healthy.",
    "They decided to {word} together as a team.",
    "It's never too late to {word} something new.",
    "The teacher encouraged us to {word} every day.",
]

NOUN_TEMPLATES = [
    "The {word} was more beautiful than I expected.",
    "I bought a new {word} at the store yesterday.",
    "This {word} reminds me of my childhood.",
    "Have you ever seen such a wonderful {word}?",
    "The {word} is an essential part of daily life.",
    "She showed me her favorite {word} collection.",
    "Every {word} has its own unique story.",
    "I can't imagine my life without this {word}.",
]

ADJ_TEMPLATES = [
    "The weather today is incredibly {word}.",
    "She has a very {word} personality.",
    "This movie was quite {word} and entertaining.",
    "He felt {word} after hearing the good news.",
    "The view from the mountain was absolutely {word}.",
    "It's {word} how quickly time passes.",
    "The food at this restaurant is always {word}.",
    "I find this book particularly {word} and insightful.",
]

_LANG_MAP = {
    "en": "en",
    "ru": "ru",
    "uz": "uz",
    "tr": "tr",
    "de": "de",
    "fr": "fr",
    "kk": "kk",
    "ar": "ar",
    "ko": "ko",
    "zh-CN": "zh-CN",
}


def translate_word(word: str, source_lang: str = "en", target_lang: str = "ru") -> dict:
    """
    Переводит английское слово на целевой язык и генерирует пример.

    Returns:
        dict: word, translation, example, target_lang
    """
    w = word.strip().lower()
    src = _LANG_MAP.get(source_lang, "en")
    dest = _LANG_MAP.get(target_lang, "ru")
    try:
        translator = GoogleTranslator(source=src, target=dest)
        translation = translator.translate(w) or ""
        if not translation.strip():
            raise ValueError("empty translation")
    except Exception as e:
        err = str(e)[:80]
        translation = (
            f"⚠️ Ошибка: {err}" if target_lang == "ru" else f"⚠️ Xato: {err}"
        )

    example = _generate_example(w)

    return {
        "word": w,
        "translation": translation,
        "example": example,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }


def _generate_example(word: str) -> str:
    all_templates = EXAMPLE_TEMPLATES + NOUN_TEMPLATES + ADJ_TEMPLATES
    template = random.choice(all_templates)
    return template.format(word=word)
