"""
Сервис перевода — обёртка над deep-translator.
Переводит слова и генерирует контекстные примеры.
Поддерживает перевод на русский и узбекский языки.
"""

import random
from deep_translator import GoogleTranslator


# Шаблоны для генерации примеров предложений
# {word} будет заменено на английское слово
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

# Шаблоны для существительных
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

# Шаблоны для прилагательных
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


def translate_word(word: str, target_lang: str = "ru") -> dict:
    """
    Переводит английское слово на целевой язык и генерирует пример.

    Args:
        word: Английское слово для перевода.
        target_lang: Язык перевода ('ru' или 'uz').

    Returns:
        dict с ключами: 'word', 'translation', 'example', 'target_lang'
    """
    try:
        # Переводим слово через Google Translate
        translator = GoogleTranslator(source='en', target=target_lang)
        translation = translator.translate(word.strip().lower())

        # Если перевод не получен — fallback
        if not translation:
            translation = "⚠️ Перевод не найден" if target_lang == "ru" else "⚠️ Tarjima topilmadi"

    except Exception as e:
        translation = f"⚠️ Ошибка: {str(e)[:50]}"

    # Генерируем пример предложения (всегда на английском)
    example = _generate_example(word.strip().lower())

    return {
        "word": word.strip().lower(),
        "translation": translation,
        "example": example,
        "target_lang": target_lang,
    }


def _generate_example(word: str) -> str:
    """
    Генерирует контекстный пример предложения со словом.
    Выбирает случайный шаблон и подставляет слово.
    """
    # Выбираем случайный набор шаблонов
    all_templates = EXAMPLE_TEMPLATES + NOUN_TEMPLATES + ADJ_TEMPLATES
    template = random.choice(all_templates)

    return template.format(word=word)
