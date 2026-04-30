"""
Обработчик добавления нового слова (или списка слов).
FSM: ожидание ввода → парсинг → перевод → сохранение в БД.

Оптимизации для больших списков (100+ слов):
- Chunking: дробление итогового сообщения на части ≤ 4096 символов
- Throttling: asyncio.sleep(0.5) каждые 5 слов для защиты от блокировки API
- Live Progress: редактирование сообщения с прогресс-баром в реальном времени
- Лимит: максимум 150 слов за один запрос
- Batched commits: коммит в БД пачками по 25 слов
"""

import re
import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Word
from states.add_word import AddWordState
from keyboards.main import main_menu_kb, cancel_kb
from services.translator import translate_word

router = Router()

# --- Константы ---
_SPLIT_PATTERN = re.compile(r"[,;\n]+")  # Разделители списка
_MAX_WORDS = 150          # Жёсткий лимит слов за один запрос
_THROTTLE_EVERY = 5       # Пауза каждые N слов
_THROTTLE_DELAY = 0.5     # Секунды паузы
_COMMIT_BATCH = 25        # Коммит в БД каждые N слов
_PROGRESS_EVERY = 5       # Обновлять прогресс-бар каждые N слов
_MSG_CHAR_LIMIT = 4000    # Безопасный лимит символов (Telegram max = 4096)
_WORDS_PER_CHUNK = 30     # Макс. слов в одном сообщении-отчёте


# --- Утилиты ---

def _parse_word_list(text: str) -> list[str]:
    """Разбивает текст на список слов по разделителям (, ; \\n)."""
    parts = _SPLIT_PATTERN.split(text)
    return [p.strip().lower() for p in parts if p.strip()]


def _validate_word(word: str) -> bool:
    """Проверяет, что слово содержит только буквы, пробелы и дефисы."""
    return bool(word) and all(c.isalpha() or c.isspace() or c == "-" for c in word)


def _make_progress_text(done: int, total: int) -> str:
    """Генерирует текст прогресс-бара: ▓▓▓▓░░░░░░ 40%"""
    pct = int(done / total * 100) if total else 0
    filled = pct // 10
    bar = "▓" * filled + "░" * (10 - filled)
    return (
        f"⏳ <b>Обработка слов...</b>\n\n"
        f"{bar}  <b>{pct}%</b>\n"
        f"Обработано: <b>{done}/{total}</b> слов"
    )


# --- Хендлеры ---

@router.message(F.text == "📝 Добавить слово")
async def start_add_word(message: Message, state: FSMContext):
    """Переход в режим ожидания слова / списка."""
    await state.set_state(AddWordState.waiting_for_word)
    await message.answer(
        "🔤 <b>Введите английское слово или список слов</b>\n\n"
        "Можно отправить одно слово или сразу несколько,\n"
        "разделив их <b>запятой</b>, <b>точкой с запятой</b> "
        "или <b>переносом строки</b>.\n\n"
        "Примеры:\n"
        "• <code>serendipity</code>\n"
        "• <code>apple, banana, orange</code>\n"
        "• <code>brave; curious; gentle</code>\n\n"
        f"📌 Максимум <b>{_MAX_WORDS}</b> слов за раз.",
        parse_mode="HTML",
        reply_markup=cancel_kb()
    )


@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    """Отмена текущего действия."""
    await state.clear()
    await callback.message.answer(
        "❌ Действие отменено. Возвращаемся в меню.",
        reply_markup=main_menu_kb()
    )
    await callback.answer()


@router.message(AddWordState.waiting_for_word)
async def process_word(message: Message, state: FSMContext, session: AsyncSession):
    """Точка входа: парсит текст и направляет в одиночный или batch режим."""
    raw_text = message.text.strip()
    words = _parse_word_list(raw_text)

    if not words:
        await message.answer("⚠️ Не удалось распознать слова. Попробуй ещё раз.", parse_mode="HTML")
        return

    # Лимит на количество слов
    if len(words) > _MAX_WORDS:
        await message.answer(
            f"⚠️ Слишком много слов! Максимум — <b>{_MAX_WORDS}</b> за раз.\n"
            f"Ты отправил <b>{len(words)}</b>. Раздели список на части.",
            parse_mode="HTML"
        )
        return

    if len(words) == 1:
        await _process_single_word(message, state, session, words[0])
    else:
        await _process_word_list(message, state, session, words)


# --- Одиночный режим ---

async def _process_single_word(
    message: Message, state: FSMContext, session: AsyncSession, word_input: str
):
    """Быстрый путь для одного слова."""
    if not _validate_word(word_input):
        await message.answer(
            "⚠️ Введите слово на <b>английском языке</b>.\n"
            "Допускаются только буквы, пробелы и дефисы.",
            parse_mode="HTML"
        )
        return

    user_id = message.from_user.id
    existing = await session.scalar(
        select(Word).where(Word.user_id == user_id, Word.word == word_input)
    )
    if existing:
        await message.answer(
            f"📌 Слово <b>{word_input}</b> уже есть в словаре!\n\n"
            f"🇷🇺 Перевод: <b>{existing.translation}</b>\n"
            f"📝 Пример: <i>{existing.example}</i>\n\n"
            "Введи другое слово или нажми ❌ Отмена.",
            parse_mode="HTML"
        )
        return

    wait_msg = await message.answer("🔄 Перевожу слово...")
    result = translate_word(word_input)

    session.add(Word(
        user_id=user_id, word=result["word"],
        translation=result["translation"],
        example=result["example"], status="new"
    ))
    await session.commit()
    await wait_msg.delete()
    await state.clear()

    await message.answer(
        f"✅ <b>Слово добавлено!</b>\n\n"
        f"🇬🇧 <b>{result['word']}</b>\n"
        f"🇷🇺 {result['translation']}\n\n"
        f"📝 <i>{result['example']}</i>\n\n"
        f"💡 Продолжай добавлять или начни тренировку!",
        reply_markup=main_menu_kb(), parse_mode="HTML"
    )


# --- Batch режим (с throttling, progress bar, batched commits) ---

async def _process_word_list(
    message: Message, state: FSMContext, session: AsyncSession, words: list[str]
):
    """
    Пакетная обработка списка слов с оптимизациями:
    1. Live progress bar (редактирование сообщения)
    2. Throttling (пауза каждые 5 слов)
    3. Batched DB commits (каждые 25 слов)
    4. Chunked output (дробление отчёта на сообщения)
    """
    user_id = message.from_user.id
    total = len(words)

    # Отправляем начальный прогресс-бар
    progress_msg = await message.answer(
        _make_progress_text(0, total), parse_mode="HTML"
    )

    added: list[dict] = []
    skipped_dup: list[str] = []
    skipped_bad: list[str] = []
    uncommitted = 0  # Счётчик слов с последнего коммита

    for i, word_input in enumerate(words, 1):
        # Валидация
        if not _validate_word(word_input):
            skipped_bad.append(word_input)
            continue

        # Дубликат
        existing = await session.scalar(
            select(Word).where(Word.user_id == user_id, Word.word == word_input)
        )
        if existing:
            skipped_dup.append(word_input)
            continue

        # Перевод
        result = translate_word(word_input)

        session.add(Word(
            user_id=user_id, word=result["word"],
            translation=result["translation"],
            example=result["example"], status="new"
        ))
        added.append(result)
        uncommitted += 1

        # Batched commit — каждые _COMMIT_BATCH слов
        if uncommitted >= _COMMIT_BATCH:
            await session.commit()
            uncommitted = 0

        # Throttling — пауза каждые _THROTTLE_EVERY слов
        if i % _THROTTLE_EVERY == 0:
            await asyncio.sleep(_THROTTLE_DELAY)

        # Обновляем прогресс-бар каждые _PROGRESS_EVERY слов
        if i % _PROGRESS_EVERY == 0 or i == total:
            try:
                await progress_msg.edit_text(
                    _make_progress_text(i, total), parse_mode="HTML"
                )
            except Exception:
                pass  # Игнорируем ошибки редактирования (rate limit и т.д.)

    # Финальный коммит остатка
    if uncommitted > 0:
        await session.commit()

    # Удаляем прогресс-бар
    try:
        await progress_msg.delete()
    except Exception:
        pass

    await state.clear()

    # Отправляем результат (с chunking)
    await _send_batch_result(message, added, skipped_dup, skipped_bad)


# --- Chunked отправка результата ---

async def _send_batch_result(
    message: Message,
    added: list[dict],
    skipped_dup: list[str],
    skipped_bad: list[str]
):
    """
    Формирует и отправляет итог пакетной обработки.
    Разбивает на несколько сообщений, если текст > 4096 символов.
    """
    # Заголовок — всегда в первом сообщении
    header = ""
    if added:
        header = f"✅ <b>Добавлено {len(added)} слов!</b>\n\n"
    else:
        header = "ℹ️ <b>Новые слова не добавлены.</b>\n\n"

    # Подвал (дубликаты + невалидные) — всегда в последнем сообщении
    footer_parts: list[str] = []
    if skipped_dup:
        # Обрезаем список дубликатов, если слишком длинный
        dup_preview = skipped_dup[:20]
        dup_list = ", ".join(w.capitalize() for w in dup_preview)
        suffix = f" и ещё {len(skipped_dup) - 20}..." if len(skipped_dup) > 20 else ""
        footer_parts.append(
            f"📌 <b>Уже в словаре ({len(skipped_dup)}):</b> {dup_list}{suffix}"
        )
    if skipped_bad:
        bad_preview = skipped_bad[:10]
        bad_list = ", ".join(bad_preview)
        suffix = f" и ещё {len(skipped_bad) - 10}..." if len(skipped_bad) > 10 else ""
        footer_parts.append(
            f"⚠️ <b>Пропущены ({len(skipped_bad)}):</b> {bad_list}{suffix}\n"
            f"    <i>(допускаются только английские буквы)</i>"
        )
    footer_parts.append("\n💡 Продолжай добавлять или начни тренировку!")
    footer = "\n".join(footer_parts)

    # Если нет добавленных слов — одно короткое сообщение
    if not added:
        await message.answer(header + footer, reply_markup=main_menu_kb(), parse_mode="HTML")
        return

    # Разбиваем добавленные слова на чанки по _WORDS_PER_CHUNK
    chunks: list[list[dict]] = []
    for i in range(0, len(added), _WORDS_PER_CHUNK):
        chunks.append(added[i:i + _WORDS_PER_CHUNK])

    # Отправляем каждый чанк отдельным сообщением
    for chunk_idx, chunk in enumerate(chunks):
        parts: list[str] = []

        # Заголовок — только в первом чанке
        if chunk_idx == 0:
            parts.append(header)

        # Нумерация с учётом предыдущих чанков
        offset = chunk_idx * _WORDS_PER_CHUNK
        for i, r in enumerate(chunk, offset + 1):
            parts.append(
                f"  {i}. 🇬🇧 <b>{r['word']}</b> — 🇷🇺 {r['translation']}\n"
                f"      📝 <i>{r['example']}</i>"
            )

        # Подвал — только в последнем чанке
        is_last = chunk_idx == len(chunks) - 1
        if is_last:
            parts.append("")
            parts.append(footer)

        text = "\n".join(parts)

        # Дополнительная защита: если текст всё ещё > лимита, обрезаем
        if len(text) > _MSG_CHAR_LIMIT:
            text = text[:_MSG_CHAR_LIMIT - 20] + "\n\n<i>...обрезано</i>"

        await message.answer(
            text,
            reply_markup=main_menu_kb() if is_last else None,
            parse_mode="HTML"
        )

        # Небольшая пауза между сообщениями, чтобы не попасть в rate limit
        if not is_last:
            await asyncio.sleep(0.3)
