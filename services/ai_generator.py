"""
AI example sentence generator (Google Gemini).
Generates one natural sentence in source language + translation in native language.
"""

import asyncio
import logging
import re

import google.generativeai as genai

from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

_MODEL_NAME = "gemini-2.0-flash"

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

# Localized fallback messages when AI generation fails
_FALLBACK_MESSAGES = {
    "en": "(AI example generation temporarily unavailable)",
    "ru": "(Генерация AI-примера временно недоступна)",
    "uz": "(AI misol yaratish vaqtinchalik mavjud emas)",
}


def _clean_line(line: str) -> str:
    """Strip markdown bold/italic markers, numbering prefixes, and label prefixes."""
    s = line.strip()
    # Remove markdown bold/italic markers: *, **, _
    s = re.sub(r"[*_]+", "", s)
    # Remove leading numbering like "1." or "1)"
    s = re.sub(r"^\d+[.)]\s*", "", s)
    # Remove known label prefixes (case-insensitive)
    s = re.sub(
        r"^(source|translation|line\s*\d*|sentence|tarjima|перевод|misol)\s*:\s*",
        "",
        s,
        flags=re.IGNORECASE,
    )
    return s.strip()


def _parse_response(text: str, word: str) -> tuple[str, str] | None:
    """
    Parse Gemini response into (source_sentence, translated_sentence).

    Accepts any two non-empty lines. Cleans markdown artifacts and label prefixes.
    Validates that the first line actually contains the word (case-insensitive).
    """
    if not text:
        return None

    lines = [_clean_line(ln) for ln in text.strip().splitlines() if _clean_line(ln)]

    if len(lines) < 2:
        return None

    source_line = lines[0]
    target_line = lines[1]

    # Basic sanity: source line should contain the word (case-insensitive)
    if word.lower() not in source_line.lower():
        # Maybe lines are swapped or the model used a different form;
        # check the second line too
        if word.lower() in target_line.lower():
            source_line, target_line = target_line, source_line
        else:
            # Accept anyway — the model may have conjugated/declined the word
            pass

    # Reject if either line is just the bare word
    if source_line.lower().strip() == word.lower().strip():
        return None
    if target_line.lower().strip() == word.lower().strip():
        return None

    return source_line, target_line


def _get_fallback(locale: str) -> str:
    """Return localized fallback message."""
    return _FALLBACK_MESSAGES.get(locale, _FALLBACK_MESSAGES["en"])


async def generate_example(
    word: str, source_lang: str, target_lang: str, locale: str = "en"
) -> dict:
    """
    Generate an AI example sentence for a word.

    Returns:
        {
            "example_source": "<sentence in source_lang>",
            "example_translation": "<translation in target_lang>"
        }

    On failure returns a clean fallback error string (never echoes the word).
    """
    w = word.strip()
    src_name = _LANG_NAMES.get(source_lang, source_lang)
    tgt_name = _LANG_NAMES.get(target_lang, target_lang)

    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set, skipping AI example generation")
        fallback = _get_fallback(locale)
        return {"example_source": fallback, "example_translation": ""}

    prompt = (
        f"Write one short, very simple everyday example sentence in {src_name} "
        f"using the word '{w}'. Then provide its direct translation in {tgt_name}.\n"
        f"Return ONLY the result in two lines, separated by a newline. "
        f"Do not use asterisks, markdown, or any introductory text.\n"
        f"Line 1: The sentence in {src_name}.\n"
        f"Line 2: The translation in {tgt_name}."
    )

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(_MODEL_NAME)
        response = await asyncio.to_thread(model.generate_content, prompt)
        raw_text = getattr(response, "text", "") or ""
        logger.debug("Gemini raw response for '%s': %s", w, repr(raw_text))

        parsed = _parse_response(raw_text, w)
        if parsed:
            source_sentence, translated_sentence = parsed
            return {
                "example_source": source_sentence,
                "example_translation": translated_sentence,
            }
        else:
            logger.warning(
                "Gemini response could not be parsed for '%s': %s", w, repr(raw_text)
            )
    except Exception as exc:
        logger.warning("Gemini example generation failed for '%s': %s", w, exc)

    # Clean fallback — never echo the bare word
    fallback = _get_fallback(locale)
    return {"example_source": fallback, "example_translation": ""}
