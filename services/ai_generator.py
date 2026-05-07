"""
AI example sentence generator (Google Gemini).
Generates one natural sentence in source language + translation in native language.
"""

import asyncio
import logging

import google.generativeai as genai

from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

_MODEL_NAME = "gemini-1.5-flash"

_LANG_NAMES = {
    "en": "English",
    "ru": "Russian",
    "uz": "Uzbek",
    "tr": "Turkish",
    "de": "German",
    "fr": "French",
    "kk": "Kazakh",
    "ar": "Arabic",
    "ko": "Korean",
    "zh-CN": "Chinese",
}


def _parse_response(text: str) -> tuple[str, str] | None:
    source_line = ""
    target_line = ""
    for raw in (text or "").splitlines():
        line = raw.strip()
        if line.lower().startswith("source:"):
            source_line = line.split(":", 1)[1].strip()
        elif line.lower().startswith("translation:"):
            target_line = line.split(":", 1)[1].strip()
    if source_line and target_line:
        return source_line, target_line
    return None


async def generate_example(word: str, source_lang: str, target_lang: str) -> dict:
    """
    Returns:
        {
            "example_source": "...",
            "example_translation": "..."
        }
    """
    w = word.strip()
    src_name = _LANG_NAMES.get(source_lang, source_lang)
    tgt_name = _LANG_NAMES.get(target_lang, target_lang)

    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set, skipping AI example generation")
        return {"example_source": w, "example_translation": w}

    prompt = (
        "You are a language learning assistant.\n"
        f'Write one short, natural sentence in {src_name} using the exact word "{w}".\n'
        f"Then provide its translation in {tgt_name}.\n"
        "Return strictly in this format:\n"
        "SOURCE: <sentence>\n"
        "TRANSLATION: <translated sentence>\n"
        "No extra text."
    )

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(_MODEL_NAME)
        response = await asyncio.to_thread(model.generate_content, prompt)
        parsed = _parse_response(getattr(response, "text", "") or "")
        if parsed:
            source_sentence, translated_sentence = parsed
            return {
                "example_source": source_sentence,
                "example_translation": translated_sentence,
            }
    except Exception as exc:
        logger.warning("Gemini example generation failed: %s", exc)

    return {"example_source": w, "example_translation": w}
