"""
Translation service — deep-translator (Google).
Translates a single word between selected languages.
"""

from deep_translator import GoogleTranslator


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
    Переводит слово с исходного языка на целевой язык.

    Returns:
        dict: word, translation, source_lang, target_lang
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

    return {
        "word": w,
        "translation": translation,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
