"""
AI example sentence generator (Google Gemini).
Generates one natural sentence in source language + translation in native language.
"""

import asyncio
import logging
import re
import sys

from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

# ── Startup diagnostic ────────────────────────────────────────────
if GEMINI_API_KEY:
    print(f"[ai_generator] ✅ GEMINI_API_KEY loaded ({len(GEMINI_API_KEY)} chars)", file=sys.stderr)
else:
    print("[ai_generator] ⚠️  GEMINI_API_KEY is EMPTY — AI examples will be disabled", file=sys.stderr)

# ── Try to import google.generativeai ─────────────────────────────
try:
    import google.generativeai as genai
    print(f"[ai_generator] ✅ google.generativeai imported OK (version={getattr(genai, '__version__', 'unknown')})", file=sys.stderr)
except ImportError as _e:
    genai = None
    print(f"[ai_generator] ❌ google.generativeai import FAILED: {_e}", file=sys.stderr)

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
        if word.lower() in target_line.lower():
            source_line, target_line = target_line, source_line

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

    # ── Guard: missing library ──
    if genai is None:
        print(f"[ai_generator] ❌ google.generativeai not installed — cannot generate for '{w}'", file=sys.stderr)
        return {"example_source": _get_fallback(locale), "example_translation": ""}

    # ── Guard: missing API key ──
    if not GEMINI_API_KEY:
        print(f"[ai_generator] ⚠️  No API key — skipping generation for '{w}'", file=sys.stderr)
        return {"example_source": _get_fallback(locale), "example_translation": ""}

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
        print(f"[ai_generator] 🔄 Calling Gemini for '{w}' ({src_name}→{tgt_name})...", file=sys.stderr)

        response = await asyncio.to_thread(model.generate_content, prompt)
        raw_text = getattr(response, "text", "") or ""
        print(f"[ai_generator] 📥 Raw response for '{w}': {repr(raw_text[:200])}", file=sys.stderr)

        parsed = _parse_response(raw_text, w)
        if parsed:
            source_sentence, translated_sentence = parsed
            print(f"[ai_generator] ✅ Parsed OK: {source_sentence!r} / {translated_sentence!r}", file=sys.stderr)
            return {
                "example_source": source_sentence,
                "example_translation": translated_sentence,
            }
        else:
            print(f"[ai_generator] ⚠️  Could not parse response for '{w}': {repr(raw_text[:300])}", file=sys.stderr)

    except Exception as exc:
        # ── CRITICAL: Print full error to terminal for debugging ──
        print(f"[ai_generator] ❌ EXCEPTION for '{w}': {type(exc).__name__}: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)

    # Clean fallback — never echo the bare word
    fallback = _get_fallback(locale)
    return {"example_source": fallback, "example_translation": ""}
