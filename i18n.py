"""
Localization module (i18n). EN / RU / UZ.
English is the default interface language.
"""

MESSAGES = {
    # ── English (default) ──────────────────────────────────────────
    "en": {
        "choose_language": "🌐 <b>Choose interface language:</b>",
        "lang_changed": "✅ Language changed to <b>English</b>.",
        "welcome": (
            "👋 Hi, <b>{name}</b>!\n\n"
            "🇬🇧 I'm a bot for learning English words.\n\n"
            "📝 <b>Add words</b> — I'll translate automatically\n"
            "🆕 <b>New words</b> — recently added\n"
            "🎯 <b>Training</b> — test your knowledge\n"
            "📊 <b>My progress</b> — your stats\n"
            "⚙️ <b>Settings</b> — change language\n\n"
            "🚀 Let's go!"
        ),
        "help": (
            "📖 <b>Help</b>\n\n"
            "Available commands:\n"
            "/start — restart the bot\n"
            "/add — add a word\n"
            "/train — start training\n"
            "/words — show new words\n"
            "/settings — change language\n"
            "/help — this message\n\n"
            "You can also use the menu buttons below."
        ),
        "btn_add_word": "📝 Add words",
        "btn_new_words": "🆕 New words",
        "btn_training": "🎯 Training",
        "btn_progress": "📊 My progress",
        "btn_settings": "⚙️ Settings",
        "input_placeholder": "Choose an action...",
        "btn_next_word": "⏭ Next word",
        "btn_hint": "💡 Hint",
        "btn_finish": "🏁 Finish",
        "btn_cancel": "❌ Cancel",
        "add_word_prompt": (
            "🔤 <b>Enter an English word or a list of words</b>\n\n"
            "Send one word or several separated by\n"
            "<b>comma</b>, <b>semicolon</b>, or <b>newline</b>.\n\n"
            "Examples:\n"
            "• <code>serendipity</code>\n"
            "• <code>apple, banana, orange</code>\n\n"
            "📌 Max <b>{max_words}</b> words at once."
        ),
        "invalid_word": "⚠️ Enter a word in <b>English</b>.\nOnly letters, spaces and hyphens allowed.",
        "word_not_recognized": "⚠️ Could not recognize words. Try again.",
        "too_many_words": "⚠️ Too many words! Max — <b>{max_words}</b>.\nYou sent <b>{count}</b>. Split the list.",
        "word_exists": "📌 <b>{word}</b> is already in your dictionary!\n\n{flag} Translation: <b>{translation}</b>\n📝 Example: <i>{example}</i>\n\nEnter another word or press ❌ Cancel.",
        "translating": "🔄 Translating…",
        "word_added": "✅ <b>Word added!</b>\n\n🇬🇧 <b>{word}</b>\n{flag} {translation}\n\n📝 <i>{example}</i>\n\n💡 Keep adding or start training!",
        "cancel_action": "❌ Action cancelled. Back to menu.",
        "progress_bar": "⏳ <b>Processing words…</b>\n\n{bar}  <b>{pct}%</b>\nProcessed: <b>{done}/{total}</b> words",
        "batch_added": "✅ <b>{count} words added!</b>\n\n",
        "batch_none_added": "ℹ️ <b>No new words added.</b>\n\n",
        "batch_duplicates": "📌 <b>Already in dictionary ({count}):</b> {list}",
        "batch_invalid": "⚠️ <b>Skipped ({count}):</b> {list}\n    <i>(only English letters allowed)</i>",
        "batch_continue": "\n💡 Keep adding or start training!",
        "new_words_empty": "🆕 <b>New words</b>\n\nNo new words to learn.\n\n📝 Press <b>Add words</b> to expand your dictionary!\nOr all words are in training — great! 🎉",
        "new_words_header": "🆕 <b>New words</b> ({count} items)\n\n",
        "new_words_footer": "💡 Press <b>🎯 Training</b> to practice these words!",
        "progress_empty": "📊 <b>Your progress</b>\n\nNo words yet.\nPress <b>📝 Add words</b> to start! 🚀",
        "progress_stats": "📊 <b>Your progress</b>\n\n📚 Total: <b>{total}</b>\n\n🆕 New: <b>{new}</b>\n📖 Learning: <b>{learning}</b>\n✅ Learned: <b>{learned}</b>\n\nProgress: {bar} {pct:.0f}%\n\n{comment}",
        "progress_great": "🔥 Great job! Keep going!",
        "progress_keep": "💪 Keep it up! Keep training!",
        "training_empty": "🎯 <b>Training</b>\n\nNo words for training yet.\nFirst add some words via <b>📝 Add words</b>! 🚀",
        "training_q_translation": "🎯 <b>Training</b> {status_emoji}\n\n{flag} Translation: <b>{translation}</b>\n\n❓ Write the English word:",
        "training_q_example": "🎯 <b>Training</b>\n\n📝 Fill in the blank:\n<i>{example}</i>\n\n{flag} Hint: {translation}\n\n❓ Write the word:",
        "training_correct": "✅ <b>Correct!</b> 🎉\n\n🇬🇧 <b>{word}</b> — {flag} {translation}\n📝 <i>{example}</i>\n\n📊 Score: <b>{score}/{total}</b>{status_text}",
        "training_incorrect": "❌ <b>Wrong!</b>\n\nYour answer: <s>{answer}</s>\nCorrect: 🇬🇧 <b>{word}</b>\n{flag} {translation}\n📝 <i>{example}</i>\n\n📊 Score: <b>{score}/{total}</b>\n\n💡 Remember it for next time!",
        "training_learned": "\n\n🏆 Word marked as <b>learned</b>!",
        "training_days_left": "\n\n📈 {days} day(s) left to «learned» status",
        "training_finished": "🏁 <b>Training finished!</b>\n\n📊 Result: <b>{score}/{total}</b>\n\n{comment}",
        "training_no_more": "🏁 <b>Training finished!</b>\n\n📊 Result: <b>{score}/{total}</b>\nNo more words. Add new ones! 🚀",
        "training_error": "⚠️ Training error. Start over.",
        "training_word_missing": "⚠️ Word not found. Restart training.",
        "hint_text": "💡 Hint: {hint} ({length} letters)",
        "hint_no_word": "⚠️ No current word",
        "hint_not_found": "⚠️ Word not found",
        "result_excellent": "🔥 Excellent! You're a master!",
        "result_good": "👍 Good result! Keep training!",
        "result_try_again": "💪 Don't give up! Practice makes perfect!",
        "result_no_answers": "Try next time! 💪",
        "settings_title": "⚙️ <b>Settings</b>\n\nChoose an action:",
        "settings_change_lang": "🌐 Change language",
    },
    # ── Russian ────────────────────────────────────────────────────
    "ru": {
        "choose_language": "🌐 <b>Выберите язык интерфейса:</b>",
        "lang_changed": "✅ Язык изменён на <b>Русский</b>.",
        "welcome": (
            "👋 Привет, <b>{name}</b>!\n\n"
            "🇬🇧 Я — бот для изучения английских слов.\n\n"
            "📝 <b>Добавить слово</b> — автоматический перевод\n"
            "🆕 <b>Новые слова</b> — недавно добавленные\n"
            "🎯 <b>Тренировка</b> — проверь знания\n"
            "📊 <b>Мой прогресс</b> — статистика\n"
            "⚙️ <b>Настройки</b> — смена языка\n\n"
            "🚀 Давай начнём!"
        ),
        "help": (
            "📖 <b>Помощь</b>\n\n"
            "Доступные команды:\n"
            "/start — перезапустить бота\n"
            "/add — добавить слово\n"
            "/train — начать тренировку\n"
            "/words — показать новые слова\n"
            "/settings — сменить язык\n"
            "/help — эта справка\n\n"
            "Также используйте кнопки меню."
        ),
        "btn_add_word": "📝 Добавить слово",
        "btn_new_words": "🆕 Новые слова",
        "btn_training": "🎯 Тренировка",
        "btn_progress": "📊 Мой прогресс",
        "btn_settings": "⚙️ Настройки",
        "input_placeholder": "Выберите действие...",
        "btn_next_word": "⏭ Следующее слово",
        "btn_hint": "💡 Подсказка",
        "btn_finish": "🏁 Закончить",
        "btn_cancel": "❌ Отмена",
        "add_word_prompt": "🔤 <b>Введите английское слово или список</b>\n\nРазделяйте <b>запятой</b>, <b>;</b> или <b>переносом строки</b>.\n\nПримеры:\n• <code>serendipity</code>\n• <code>apple, banana, orange</code>\n\n📌 Максимум <b>{max_words}</b> слов.",
        "invalid_word": "⚠️ Введите слово на <b>английском</b>.\nТолько буквы, пробелы и дефисы.",
        "word_not_recognized": "⚠️ Не удалось распознать. Попробуй ещё раз.",
        "too_many_words": "⚠️ Максимум — <b>{max_words}</b>. Ты отправил <b>{count}</b>.",
        "word_exists": "📌 <b>{word}</b> уже в словаре!\n\n{flag} Перевод: <b>{translation}</b>\n📝 <i>{example}</i>\n\nВведи другое или ❌ Отмена.",
        "translating": "🔄 Перевожу…",
        "word_added": "✅ <b>Слово добавлено!</b>\n\n🇬🇧 <b>{word}</b>\n{flag} {translation}\n\n📝 <i>{example}</i>\n\n💡 Продолжай или начни тренировку!",
        "cancel_action": "❌ Отменено. Возвращаемся в меню.",
        "progress_bar": "⏳ <b>Обработка…</b>\n\n{bar}  <b>{pct}%</b>\nОбработано: <b>{done}/{total}</b>",
        "batch_added": "✅ <b>Добавлено {count} слов!</b>\n\n",
        "batch_none_added": "ℹ️ <b>Новые слова не добавлены.</b>\n\n",
        "batch_duplicates": "📌 <b>Уже в словаре ({count}):</b> {list}",
        "batch_invalid": "⚠️ <b>Пропущены ({count}):</b> {list}\n    <i>(только английские буквы)</i>",
        "batch_continue": "\n💡 Продолжай или начни тренировку!",
        "new_words_empty": "🆕 <b>Новые слова</b>\n\nНет новых слов.\n📝 Нажми <b>Добавить слово</b>!\nИли все в тренировке — 🎉",
        "new_words_header": "🆕 <b>Новые слова</b> ({count} шт.)\n\n",
        "new_words_footer": "💡 Нажми <b>🎯 Тренировка</b>, чтобы закрепить!",
        "progress_empty": "📊 <b>Прогресс</b>\n\nНет слов. Нажми <b>📝 Добавить слово</b>! 🚀",
        "progress_stats": "📊 <b>Прогресс</b>\n\n📚 Всего: <b>{total}</b>\n\n🆕 Новые: <b>{new}</b>\n📖 Изучаются: <b>{learning}</b>\n✅ Выучены: <b>{learned}</b>\n\n{bar} {pct:.0f}%\n\n{comment}",
        "progress_great": "🔥 Отличная работа!",
        "progress_keep": "💪 Так держать!",
        "training_empty": "🎯 <b>Тренировка</b>\n\nНет слов. Добавь через <b>📝 Добавить слово</b>! 🚀",
        "training_q_translation": "🎯 <b>Тренировка</b> {status_emoji}\n\n{flag} Перевод: <b>{translation}</b>\n\n❓ Напиши английское слово:",
        "training_q_example": "🎯 <b>Тренировка</b>\n\n📝 Заполни пропуск:\n<i>{example}</i>\n\n{flag} Подсказка: {translation}\n\n❓ Напиши слово:",
        "training_correct": "✅ <b>Правильно!</b> 🎉\n\n🇬🇧 <b>{word}</b> — {flag} {translation}\n📝 <i>{example}</i>\n\n📊 Счёт: <b>{score}/{total}</b>{status_text}",
        "training_incorrect": "❌ <b>Неверно!</b>\n\nТвой ответ: <s>{answer}</s>\nПравильно: 🇬🇧 <b>{word}</b>\n{flag} {translation}\n📝 <i>{example}</i>\n\n📊 Счёт: <b>{score}/{total}</b>\n\n💡 Запомни!",
        "training_learned": "\n\n🏆 Слово <b>выучено</b>!",
        "training_days_left": "\n\n📈 Осталось {days} дн.",
        "training_finished": "🏁 <b>Тренировка завершена!</b>\n\n📊 Результат: <b>{score}/{total}</b>\n\n{comment}",
        "training_no_more": "🏁 <b>Завершено!</b>\n\n📊 <b>{score}/{total}</b>\nНет слов. Добавь новые! 🚀",
        "training_error": "⚠️ Ошибка. Начни заново.",
        "training_word_missing": "⚠️ Слово не найдено.",
        "hint_text": "💡 {hint} ({length} букв)",
        "hint_no_word": "⚠️ Нет слова",
        "hint_not_found": "⚠️ Не найдено",
        "result_excellent": "🔥 Великолепно!",
        "result_good": "👍 Хорошо! Продолжай!",
        "result_try_again": "💪 Не сдавайся!",
        "result_no_answers": "Попробуй ещё! 💪",
        "settings_title": "⚙️ <b>Настройки</b>\n\nВыберите:",
        "settings_change_lang": "🌐 Сменить язык",
    },
    # ── Uzbek ──────────────────────────────────────────────────────
    "uz": {
        "choose_language": "🌐 <b>Interfeys tilini tanlang:</b>",
        "lang_changed": "✅ Til <b>O'zbekcha</b>ga o'zgartirildi.",
        "welcome": (
            "👋 Salom, <b>{name}</b>!\n\n"
            "🇬🇧 Men ingliz so'zlarni o'rganish botiman.\n\n"
            "📝 <b>So'z qo'shish</b> — avtomatik tarjima\n"
            "🆕 <b>Yangi so'zlar</b> — yaqinda qo'shilgan\n"
            "🎯 <b>Mashq</b> — bilimingizni sinang\n"
            "📊 <b>Natijalarim</b> — statistika\n"
            "⚙️ <b>Sozlamalar</b> — tilni o'zgartirish\n\n"
            "🚀 Boshlaylik!"
        ),
        "help": (
            "📖 <b>Yordam</b>\n\n"
            "Buyruqlar:\n"
            "/start — botni qayta ishga tushirish\n"
            "/add — so'z qo'shish\n"
            "/train — mashq boshlash\n"
            "/words — yangi so'zlar\n"
            "/settings — tilni o'zgartirish\n"
            "/help — ushbu xabar\n\n"
            "Menyu tugmalaridan ham foydalaning."
        ),
        "btn_add_word": "📝 So'z qo'shish",
        "btn_new_words": "🆕 Yangi so'zlar",
        "btn_training": "🎯 Mashq",
        "btn_progress": "📊 Natijalarim",
        "btn_settings": "⚙️ Sozlamalar",
        "input_placeholder": "Amalni tanlang...",
        "btn_next_word": "⏭ Keyingi so'z",
        "btn_hint": "💡 Yordam",
        "btn_finish": "🏁 Tugatish",
        "btn_cancel": "❌ Bekor qilish",
        "add_word_prompt": "🔤 <b>Inglizcha so'z kiriting</b>\n\n<b>vergul</b>, <b>;</b> yoki <b>yangi qator</b> bilan ajrating.\n\nMisollar:\n• <code>serendipity</code>\n• <code>apple, banana, orange</code>\n\n📌 Eng ko'pi <b>{max_words}</b> ta.",
        "invalid_word": "⚠️ <b>Ingliz tilida</b> so'z kiriting.",
        "word_not_recognized": "⚠️ Aniqlab bo'lmadi. Qaytadan urinib ko'ring.",
        "too_many_words": "⚠️ Eng ko'pi — <b>{max_words}</b>. Siz <b>{count}</b> ta yubordingiz.",
        "word_exists": "📌 <b>{word}</b> allaqachon bor!\n\n{flag} Tarjima: <b>{translation}</b>\n📝 <i>{example}</i>\n\nBoshqa so'z kiriting yoki ❌ Bekor.",
        "translating": "🔄 Tarjima qilinmoqda…",
        "word_added": "✅ <b>So'z qo'shildi!</b>\n\n🇬🇧 <b>{word}</b>\n{flag} {translation}\n\n📝 <i>{example}</i>\n\n💡 Davom eting yoki mashq boshlang!",
        "cancel_action": "❌ Bekor qilindi. Menyuga qaytamiz.",
        "progress_bar": "⏳ <b>Qayta ishlanmoqda…</b>\n\n{bar}  <b>{pct}%</b>\n<b>{done}/{total}</b>",
        "batch_added": "✅ <b>{count} ta so'z qo'shildi!</b>\n\n",
        "batch_none_added": "ℹ️ <b>Yangi so'zlar qo'shilmadi.</b>\n\n",
        "batch_duplicates": "📌 <b>Allaqachon bor ({count}):</b> {list}",
        "batch_invalid": "⚠️ <b>O'tkazildi ({count}):</b> {list}",
        "batch_continue": "\n💡 Davom eting yoki mashq boshlang!",
        "new_words_empty": "🆕 <b>Yangi so'zlar</b>\n\nYangi so'zlar yo'q.\n📝 <b>So'z qo'shish</b> tugmasini bosing! 🎉",
        "new_words_header": "🆕 <b>Yangi so'zlar</b> ({count} ta)\n\n",
        "new_words_footer": "💡 <b>🎯 Mashq</b> tugmasini bosing!",
        "progress_empty": "📊 <b>Natija</b>\n\nSo'zlar yo'q. <b>📝 So'z qo'shish</b>! 🚀",
        "progress_stats": "📊 <b>Natija</b>\n\n📚 Jami: <b>{total}</b>\n\n🆕 Yangi: <b>{new}</b>\n📖 O'rganilmoqda: <b>{learning}</b>\n✅ O'rganilgan: <b>{learned}</b>\n\n{bar} {pct:.0f}%\n\n{comment}",
        "progress_great": "🔥 Ajoyib!",
        "progress_keep": "💪 Davom eting!",
        "training_empty": "🎯 <b>Mashq</b>\n\nSo'zlar yo'q. <b>📝 So'z qo'shish</b>! 🚀",
        "training_q_translation": "🎯 <b>Mashq</b> {status_emoji}\n\n{flag} Tarjima: <b>{translation}</b>\n\n❓ Inglizcha so'zni yozing:",
        "training_q_example": "🎯 <b>Mashq</b>\n\n📝 To'ldiring:\n<i>{example}</i>\n\n{flag} Yordam: {translation}\n\n❓ So'zni yozing:",
        "training_correct": "✅ <b>To'g'ri!</b> 🎉\n\n🇬🇧 <b>{word}</b> — {flag} {translation}\n📝 <i>{example}</i>\n\n📊 <b>{score}/{total}</b>{status_text}",
        "training_incorrect": "❌ <b>Noto'g'ri!</b>\n\nJavobingiz: <s>{answer}</s>\nTo'g'ri: 🇬🇧 <b>{word}</b>\n{flag} {translation}\n📝 <i>{example}</i>\n\n📊 <b>{score}/{total}</b>\n\n💡 Eslab qoling!",
        "training_learned": "\n\n🏆 So'z <b>o'rganilgan</b>!",
        "training_days_left": "\n\n📈 {days} kun qoldi",
        "training_finished": "🏁 <b>Mashq tugadi!</b>\n\n📊 <b>{score}/{total}</b>\n\n{comment}",
        "training_no_more": "🏁 <b>Tugadi!</b>\n\n📊 <b>{score}/{total}</b>\nSo'zlar yo'q. Yangi qo'shing! 🚀",
        "training_error": "⚠️ Xato. Qaytadan boshlang.",
        "training_word_missing": "⚠️ So'z topilmadi.",
        "hint_text": "💡 {hint} ({length} harf)",
        "hint_no_word": "⚠️ So'z yo'q",
        "hint_not_found": "⚠️ Topilmadi",
        "result_excellent": "🔥 Ajoyib!",
        "result_good": "👍 Yaxshi!",
        "result_try_again": "💪 Davom eting!",
        "result_no_answers": "Keyingi safar! 💪",
        "settings_title": "⚙️ <b>Sozlamalar</b>\n\nTanlang:",
        "settings_change_lang": "🌐 Tilni o'zgartirish",
    },
}

# Flag emoji per locale
LOCALE_FLAGS = {"en": "🇷🇺", "ru": "🇷🇺", "uz": "🇺🇿"}

# Translation target language per locale (en defaults to ru)
LOCALE_TARGET_LANG = {"en": "ru", "ru": "ru", "uz": "uz"}

# All known button texts across all locales (for filters)
def _collect_btn(key: str) -> list[str]:
    return list({MESSAGES[loc][key] for loc in MESSAGES if key in MESSAGES[loc]})

BTN_ADD_WORD = _collect_btn("btn_add_word")
BTN_NEW_WORDS = _collect_btn("btn_new_words")
BTN_TRAINING = _collect_btn("btn_training")
BTN_PROGRESS = _collect_btn("btn_progress")
BTN_SETTINGS = _collect_btn("btn_settings")

DEFAULT_LOCALE = "en"


def t(locale: str, key: str, **kwargs) -> str:
    """Return localized string by key with variable substitution."""
    lang = MESSAGES.get(locale, MESSAGES[DEFAULT_LOCALE])
    template = lang.get(key, MESSAGES[DEFAULT_LOCALE].get(key, f"[{key}]"))
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template
    return template


def get_flag(locale: str) -> str:
    """Return emoji flag for locale."""
    return LOCALE_FLAGS.get(locale, "🇷🇺")


def get_target_lang(locale: str) -> str:
    """Return translation target language code for locale."""
    return LOCALE_TARGET_LANG.get(locale, "ru")
