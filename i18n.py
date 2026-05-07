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
            "📚 I'm a bot for learning vocabulary.\n"
            "{source_flag} <b>{source_name}</b> → {target_flag} <b>{target_name}</b>\n\n"
            "🎯 <b>Practice</b> — spaced repetition training\n"
            "📝 <b>Add words</b> — auto translation\n"
            "📊 <b>My progress</b> — stats\n"
            "🗂 <b>My vocabulary</b> — your list\n"
            "⚙️ <b>Settings</b> — change languages\n\n"
            "💡 <code>/learn</code> — browse recent new words\n\n"
            "🚀 Let's go!"
        ),
        "help": (
            "📖 <b>Help</b>\n\n"
            "Available commands:\n"
            "/start — restart the bot\n"
            "/add — add a word\n"
            "/train — start training\n"
            "/learn — show new words\n"
            "/words — my vocabulary (pages)\n"
            "/stats — progress summary\n"
            "/settings — translation language\n"
            "/help — this message\n\n"
            "You can also use the menu buttons below."
        ),
        "btn_add_words": "📝 Add words",
        "btn_train": "🎯 Practice",
        "btn_learn_new": "📖 Learn New",
        "btn_results": "📊 My progress",
        "btn_vocabulary": "🗂 My vocabulary",
        "btn_my_words": "🗂 My vocabulary",
        "btn_settings": "⚙️ Settings",
        "btn_prev_page": "Previous",
        "btn_next_page": "Next",
        "btn_mode_translation": "🔄 Translation → English",
        "btn_mode_sentence": "📝 Complete the sentence",
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
        "word_added": "✅ <b>Word added!</b>\n\n{source_flag} <b>{word}</b>\n{flag} {translation}\n\n📝 <i>{example}</i>\n\n💡 Keep adding or start training!",
        "cancel_action": "❌ Action cancelled. Back to menu.",
        "progress_bar": "⏳ <b>Processing words…</b>\n\n{bar}  <b>{pct}%</b>\nProcessed: <b>{done}/{total}</b> words",
        "batch_added": "✅ <b>Added {count} words!</b>\n\n",
        "batch_none_added": "ℹ️ <b>No new words added.</b>\n\n",
        "batch_duplicates": "📌 <b>Already in dictionary ({count}):</b> {list}",
        "batch_invalid": "⚠️ <b>Skipped ({count}):</b> {list}\n    <i>(only English letters allowed)</i>",
        "batch_continue": "\n💡 Keep adding or start training!",
        "batch_started": "⏳ <b>Processing {count} words…</b>\nYou'll get reports in short chunks.",
        "learn_empty": "📖 <b>Learn New</b>\n\nNo new words to learn.\n\n📝 Press <b>Add words</b> to expand your dictionary!\nOr all words are in training — great! 🎉",
        "learn_header": "📖 <b>Learn New</b> ({count} items)\n\n",
        "learn_footer": "💡 Press <b>🎯 Practice</b> to train these words!",
        "training_cancelled_menu": "⏹ Training stopped (menu). Tap <b>🎯 Practice</b> to start again.",
        "my_words_empty": "🗂 <b>My vocabulary</b>\n\nNo words yet.\nPress <b>📝 Add words</b> to start! 🚀",
        "my_stats_empty": "📊 <b>My progress</b>\n\nNo words yet.\nAdd words to see stats! 🚀",
        "my_stats_header": (
            "📊 <b>My progress</b>\n\n"
            "📚 Total: <b>{total}</b> | 🆕 New: <b>{new}</b> | ✅ Learned: <b>{learned}</b>\n\n"
            "{bar} <b>{pct:.0f}%</b> learned\n"
        ),
        "my_words_header": "📊 <b>Your Deck Stats</b>\n\n📚 Total: <b>{total}</b>\n\n🆕 New: <b>{new}</b>\n⏳ Learning: <b>{learning}</b>\n✅ Learned: <b>{learned}</b>\n\nKeep up the good work! 🚀\n",
        "words_page_title": "🗂 <b>My vocabulary</b> <i>({page}/{total_pages})</i>\n\n",
        "training_empty": "🎯 <b>Practice</b>\n\nNo words to train yet.\nAdd words first! 🚀",
        "training_pick_mode": "🎯 <b>Practice</b>\n\nChoose a mode:",
        "training_translation_ask": (
            "🎯 <b>Translation → {source_name}</b>\n\n"
            "{flag} Translation: <b>{translation}</b>\n\n"
            "✏️ Type the <b>{source_name}</b> word:"
        ),
        "training_sentence_ask": (
            "🎯 <b>Complete the sentence</b>\n\n"
            "📝 <i>{example}</i>\n\n"
            "✏️ Type the missing word:"
        ),
        "training_question": "🧠 <b>Training</b>\n\n📝 Fill in the blank:\n<i>{example}</i>\n\n{flag} Hint: {translation}\n\n❓ Choose the correct word:",
        "training_correct": "✅ <b>Correct!</b> 🎉\n\n{source_flag} <b>{word}</b> — {flag} {translation}\n📝 <i>{example}</i>\n\n📊 Score: <b>{score}/{total}</b>{status_text}",
        "training_incorrect": "❌ <b>Wrong!</b>\n\nCorrect: {source_flag} <b>{word}</b>\n{flag} {translation}\n📝 <i>{example}</i>\n\n📊 Score: <b>{score}/{total}</b>\n\n💡 Remember it for next time!",
        "training_learned": "\n\n🏆 Word marked as <b>learned</b>!",
        "training_progress": "\n\n📈 {left} more correct answer(s) to «learned»",
        "training_finished": "🏁 <b>Training finished!</b>\n\n📊 Result: <b>{score}/{total}</b>\n\n{comment}",
        "training_no_more": "🏁 <b>Training finished!</b>\n\n📊 Result: <b>{score}/{total}</b>\nNo more words. Add new ones! 🚀",
        "hint_text": "💡 Hint: {hint} ({length} letters)",
        "hint_example_sentence": "📝 Example: {example}",
        "hint_no_word": "⚠️ No current word",
        "hint_not_found": "⚠️ Word not found",
        "result_excellent": "🔥 Excellent! You're a master!",
        "result_good": "👍 Good result! Keep training!",
        "result_try_again": "💪 Don't give up! Practice makes perfect!",
        "result_no_answers": "Try next time! 💪",
        "settings_title": "⚙️ <b>Settings</b>\n\n🌐 Source language: <b>{source}</b>\n🔤 Native language: <b>{native}</b>\n\nChoose an action:",
        "settings_change_source": "🌐 Source language",
        "settings_change_target": "🔤 Native language",
        "choose_source_lang": "🌐 <b>Choose source language:</b>\n\nThis is the language you want to learn.",
        "choose_target_lang": "🔤 <b>Choose native language:</b>\n\nTranslations and explanations will use this language.",
        "source_lang_changed": "✅ Source language changed to <b>{lang}</b>.",
        "target_lang_changed": "✅ Native language changed to <b>{lang}</b>.",
    },
    # ── Russian ────────────────────────────────────────────────────
    "ru": {
        "choose_language": "🌐 <b>Выберите язык интерфейса:</b>",
        "lang_changed": "✅ Язык изменён на <b>Русский</b>.",
        "welcome": (
            "👋 Привет, <b>{name}</b>!\n\n"
            "📚 Я — бот для изучения слов.\n"
            "{source_flag} <b>{source_name}</b> → {target_flag} <b>{target_name}</b>\n\n"
            "➕ <b>Добавить слова</b> — автоматический перевод\n"
            "📖 <b>Учить новые</b> — недавно добавленные\n"
            "🧠 <b>Тренировка</b> — проверь знания\n"
            "🗂 <b>Мои слова</b> — твой словарь\n"
            "⚙️ <b>Настройки</b> — смена языков\n\n"
            "🚀 Давай начнём!"
        ),
        "help": (
            "📖 <b>Помощь</b>\n\n"
            "Доступные команды:\n"
            "/start — перезапустить бота\n"
            "/add — добавить слово\n"
            "/train — начать тренировку\n"
            "/learn — показать новые слова\n"
            "/words — мои слова\n"
            "/settings — сменить язык\n"
            "/help — эта справка\n\n"
            "Также используйте кнопки меню."
        ),
        "btn_add_words": "📝 Добавить слова",
        "btn_train": "🎯 Тренировка",
        "btn_learn_new": "📖 Учить новые",
        "btn_results": "📊 Мои результаты",
        "btn_vocabulary": "🗂 Мои слова",
        "btn_my_words": "🗂 Мои слова",
        "btn_settings": "⚙️ Настройки",
        "btn_prev_page": "Назад",
        "btn_next_page": "Далее",
        "btn_mode_translation": "🔄 Перевод → английский",
        "btn_mode_sentence": "📝 Предложение с пропуском",
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
        "word_added": "✅ <b>Слово добавлено!</b>\n\n{source_flag} <b>{word}</b>\n{flag} {translation}\n\n📝 <i>{example}</i>\n\n💡 Продолжай или начни тренировку!",
        "cancel_action": "❌ Отменено. Возвращаемся в меню.",
        "progress_bar": "⏳ <b>Обработка…</b>\n\n{bar}  <b>{pct}%</b>\nОбработано: <b>{done}/{total}</b>",
        "batch_added": "✅ <b>Добавлено {count} слов!</b>\n\n",
        "batch_none_added": "ℹ️ <b>Новые слова не добавлены.</b>\n\n",
        "batch_duplicates": "📌 <b>Уже в словаре ({count}):</b> {list}",
        "batch_invalid": "⚠️ <b>Пропущены ({count}):</b> {list}\n    <i>(только английские буквы)</i>",
        "batch_continue": "\n💡 Продолжай или начни тренировку!",
        "batch_started": "⏳ <b>Обрабатываю {count} слов…</b>\nОтчёты придут частями.",
        "learn_empty": "📖 <b>Учить новые</b>\n\nНет новых слов.\n📝 Нажми <b>Добавить слова</b>!\nИли все в тренировке — 🎉",
        "training_cancelled_menu": "⏹ Тренировка остановлена. Нажми <b>🎯 Тренировка</b>, чтобы начать снова.",
        "learn_header": "📖 <b>Учить новые</b> ({count} шт.)\n\n",
        "learn_footer": "💡 Нажми <b>🎯 Тренировка</b>, чтобы закрепить!",
        "my_words_empty": "🗂 <b>Мои слова</b>\n\nНет слов. Нажми <b>📝 Добавить слова</b>! 🚀",
        "my_stats_empty": "📊 <b>Мои результаты</b>\n\nПока нет слов. Добавь слова! 🚀",
        "my_stats_header": (
            "📊 <b>Мои результаты</b>\n\n"
            "📚 Всего: <b>{total}</b> | 🆕 Новые: <b>{new}</b> | ✅ Выучены: <b>{learned}</b>\n\n"
            "{bar} <b>{pct:.0f}%</b> выучено\n"
        ),
        "my_words_header": "🗂 <b>Мои слова</b>\n\n📚 Всего: <b>{total}</b> | 🆕 Новые: <b>{new}</b> | ✅ Выучены: <b>{learned}</b>\n\nПрогресс: {bar} {pct:.0f}%\n\n",
        "words_page_title": "🗂 <b>Мои слова</b> <i>({page}/{total_pages})</i>\n\n",
        "my_words_section_new": "🆕 <b>Новые слова:</b>\n",
        "my_words_section_learned": "\n✅ <b>Выученные слова:</b>\n",
        "training_empty": "🎯 <b>Тренировка</b>\n\nНет слов. Добавь через <b>📝 Добавить слова</b>! 🚀",
        "training_pick_mode": "🎯 <b>Тренировка</b>\n\nВыбери режим:",
        "training_translation_ask": (
            "🎯 <b>Перевод → {source_name}</b>\n\n"
            "{flag} Перевод: <b>{translation}</b>\n\n"
            "✏️ Введи слово на <b>{source_name}</b>:"
        ),
        "training_sentence_ask": (
            "🎯 <b>Предложение с пропуском</b>\n\n"
            "📝 <i>{example}</i>\n\n"
            "✏️ Введи пропущенное слово:"
        ),
        "training_question": "🧠 <b>Тренировка</b>\n\n📝 Заполни пропуск:\n<i>{example}</i>\n\n{flag} Подсказка: {translation}\n\n❓ Выбери правильное слово:",
        "training_correct": "✅ <b>Правильно!</b> 🎉\n\n{source_flag} <b>{word}</b> — {flag} {translation}\n📝 <i>{example}</i>\n\n📊 Счёт: <b>{score}/{total}</b>{status_text}",
        "training_incorrect": "❌ <b>Неверно!</b>\n\nПравильно: {source_flag} <b>{word}</b>\n{flag} {translation}\n📝 <i>{example}</i>\n\n📊 Счёт: <b>{score}/{total}</b>\n\n💡 Запомни!",
        "training_learned": "\n\n🏆 Слово <b>выучено</b>!",
        "training_progress": "\n\n📈 Ещё {left} правильных до «выучено»",
        "training_finished": "🏁 <b>Тренировка завершена!</b>\n\n📊 Результат: <b>{score}/{total}</b>\n\n{comment}",
        "training_no_more": "🏁 <b>Завершено!</b>\n\n📊 <b>{score}/{total}</b>\nНет слов. Добавь новые! 🚀",
        "hint_text": "💡 {hint} ({length} букв)",
        "hint_example_sentence": "📝 Пример: {example}",
        "hint_no_word": "⚠️ Нет слова",
        "hint_not_found": "⚠️ Не найдено",
        "result_excellent": "🔥 Великолепно!",
        "result_good": "👍 Хорошо! Продолжай!",
        "result_try_again": "💪 Не сдавайся!",
        "result_no_answers": "Попробуй ещё! 💪",
        "settings_title": "⚙️ <b>Настройки</b>\n\n🌐 Исходный язык: <b>{source}</b>\n🔤 Родной язык: <b>{native}</b>\n\nВыберите:",
        "settings_change_lang": "🌐 Сменить язык интерфейса",
        "settings_change_source": "🌐 Исходный язык",
        "settings_change_target": "🔤 Родной язык",
        "choose_source_lang": "🌐 <b>Выберите исходный язык:</b>\n\nЭто язык, который вы хотите учить.",
        "choose_target_lang": "🔤 <b>Выберите родной язык:</b>\n\nПереводы и объяснения будут на этом языке.",
        "source_lang_changed": "✅ Исходный язык изменён на <b>{lang}</b>.",
        "target_lang_changed": "✅ Родной язык изменён на <b>{lang}</b>.",
    },
    # ── Uzbek ──────────────────────────────────────────────────────
    "uz": {
        "choose_language": "🌐 <b>Interfeys tilini tanlang:</b>",
        "lang_changed": "✅ Til <b>O'zbekcha</b>ga o'zgartirildi.",
        "welcome": (
            "👋 Salom, <b>{name}</b>!\n\n"
            "📚 Men so'zlarni o'rganish botiman.\n"
            "{source_flag} <b>{source_name}</b> → {target_flag} <b>{target_name}</b>\n\n"
            "➕ <b>So'z qo'shish</b> — avtomatik tarjima\n"
            "📖 <b>Yangilarni o'rganish</b> — yaqinda qo'shilgan\n"
            "🧠 <b>Mashq</b> — bilimingizni sinang\n"
            "🗂 <b>So'zlarim</b> — lug'atingiz\n"
            "⚙️ <b>Sozlamalar</b> — tillarni o'zgartirish\n\n"
            "🚀 Boshlaylik!"
        ),
        "help": (
            "📖 <b>Yordam</b>\n\n"
            "Buyruqlar:\n"
            "/start — botni qayta ishga tushirish\n"
            "/add — so'z qo'shish\n"
            "/train — mashq boshlash\n"
            "/learn — yangi so'zlar\n"
            "/words — mening so'zlarim\n"
            "/settings — tilni o'zgartirish\n"
            "/help — ushbu xabar\n\n"
            "Menyu tugmalaridan ham foydalaning."
        ),
        "btn_add_words": "📝 So'z qo'shish",
        "btn_train": "🎯 Mashq qilish",
        "btn_learn_new": "📖 Yangilarni o'rganish",
        "btn_results": "📊 Mening natijalarim",
        "btn_vocabulary": "🗂 Mening so'zlarim",
        "btn_my_words": "🗂 Mening so'zlarim",
        "btn_settings": "⚙️ Sozlamalar",
        "btn_prev_page": "Oldingi",
        "btn_next_page": "Keyingi",
        "btn_mode_translation": "🔄 Tarjima → inglizcha",
        "btn_mode_sentence": "📝 Gapni to'ldirish",
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
        "word_added": "✅ <b>So'z qo'shildi!</b>\n\n{source_flag} <b>{word}</b>\n{flag} {translation}\n\n📝 <i>{example}</i>\n\n💡 Davom eting yoki mashq boshlang!",
        "cancel_action": "❌ Bekor qilindi. Menyuga qaytamiz.",
        "progress_bar": "⏳ <b>Qayta ishlanmoqda…</b>\n\n{bar}  <b>{pct}%</b>\n<b>{done}/{total}</b>",
        "batch_added": "✅ <b>{count} ta so'z qo'shildi!</b>\n\n",
        "batch_none_added": "ℹ️ <b>Yangi so'zlar qo'shilmadi.</b>\n\n",
        "batch_duplicates": "📌 <b>Allaqachon bor ({count}):</b> {list}",
        "batch_invalid": "⚠️ <b>O'tkazildi ({count}):</b> {list}",
        "batch_continue": "\n💡 Davom eting yoki mashq boshlang!",
        "batch_started": "⏳ <b>{count} ta so'z qayta ishlanmoqda…</b>\nHisobotlar qismlarga bo'lib keladi.",
        "learn_empty": "📖 <b>Yangilarni o'rganish</b>\n\nYangi so'zlar yo'q.\n📝 <b>So'z qo'shish</b> tugmasini bosing! 🎉",
        "training_cancelled_menu": "⏹ Mashq to'xtatildi. Qayta boshlash uchun <b>🎯 Mashq qilish</b>ni bosing.",
        "learn_header": "📖 <b>Yangilarni o'rganish</b> ({count} ta)\n\n",
        "learn_footer": "💡 <b>🎯 Mashq qilish</b> tugmasini bosing!",
        "my_words_empty": "🗂 <b>Mening so'zlarim</b>\n\nSo'zlar yo'q. <b>📝 So'z qo'shish</b>! 🚀",
        "my_stats_empty": "📊 <b>Mening natijalarim</b>\n\nHali so'zlar yo'q. 🚀",
        "my_stats_header": (
            "📊 <b>Mening natijalarim</b>\n\n"
            "📚 Jami: <b>{total}</b> | 🆕 Yangi: <b>{new}</b> | ✅ O'rganilgan: <b>{learned}</b>\n\n"
            "{bar} <b>{pct:.0f}%</b> o'rganilgan\n"
        ),
        "my_words_header": "🗂 <b>So'zlarim</b>\n\n📚 Jami: <b>{total}</b> | 🆕 Yangi: <b>{new}</b> | ✅ O'rganilgan: <b>{learned}</b>\n\nProgress: {bar} {pct:.0f}%\n\n",
        "words_page_title": "🗂 <b>Mening so'zlarim</b> <i>({page}/{total_pages})</i>\n\n",
        "my_words_section_new": "🆕 <b>Yangi so'zlar:</b>\n",
        "my_words_section_learned": "\n✅ <b>O'rganilgan so'zlar:</b>\n",
        "training_empty": "🎯 <b>Mashq</b>\n\nSo'zlar yo'q. <b>📝 So'z qo'shish</b>! 🚀",
        "training_pick_mode": "🎯 <b>Mashq</b>\n\nRejimni tanlang:",
        "training_translation_ask": (
            "🎯 <b>Tarjima → {source_name}</b>\n\n"
            "{flag} Tarjima: <b>{translation}</b>\n\n"
            "✏️ <b>{source_name}</b> so'zni yozing:"
        ),
        "training_sentence_ask": (
            "🎯 <b>Gapni to'ldirish</b>\n\n"
            "📝 <i>{example}</i>\n\n"
            "✏️ Yetishmayotgan so'zni yozing:"
        ),
        "training_question": "🧠 <b>Mashq</b>\n\n📝 To'ldiring:\n<i>{example}</i>\n\n{flag} Yordam: {translation}\n\n❓ To'g'ri so'zni tanlang:",
        "training_correct": "✅ <b>To'g'ri!</b> 🎉\n\n{source_flag} <b>{word}</b> — {flag} {translation}\n📝 <i>{example}</i>\n\n📊 <b>{score}/{total}</b>{status_text}",
        "training_incorrect": "❌ <b>Noto'g'ri!</b>\n\nTo'g'ri: {source_flag} <b>{word}</b>\n{flag} {translation}\n📝 <i>{example}</i>\n\n📊 <b>{score}/{total}</b>\n\n💡 Eslab qoling!",
        "training_learned": "\n\n🏆 So'z <b>o'rganilgan</b>!",
        "training_progress": "\n\n📈 Yana {left} ta to'g'ri javob kerak",
        "training_finished": "🏁 <b>Mashq tugadi!</b>\n\n📊 <b>{score}/{total}</b>\n\n{comment}",
        "training_no_more": "🏁 <b>Tugadi!</b>\n\n📊 <b>{score}/{total}</b>\nSo'zlar yo'q. Yangi qo'shing! 🚀",
        "hint_text": "💡 {hint} ({length} harf)",
        "hint_example_sentence": "📝 Misol: {example}",
        "hint_no_word": "⚠️ So'z yo'q",
        "hint_not_found": "⚠️ Topilmadi",
        "result_excellent": "🔥 Ajoyib!",
        "result_good": "👍 Yaxshi!",
        "result_try_again": "💪 Davom eting!",
        "result_no_answers": "Keyingi safar! 💪",
        "settings_title": "⚙️ <b>Sozlamalar</b>\n\n🌐 Manba tili: <b>{source}</b>\n🔤 Ona tili: <b>{native}</b>\n\nTanlang:",
        "settings_change_lang": "🌐 Interfeys tilini o'zgartirish",
        "settings_change_source": "🌐 Manba tili",
        "settings_change_target": "🔤 Ona tili",
        "choose_source_lang": "🌐 <b>Manba tilini tanlang:</b>\n\nBu siz o'rganmoqchi bo'lgan til.",
        "choose_target_lang": "🔤 <b>Ona tilingizni tanlang:</b>\n\nTarjima va izohlar shu tilda bo'ladi.",
        "source_lang_changed": "✅ Manba tili <b>{lang}</b>ga o'zgartirildi.",
        "target_lang_changed": "✅ Ona tili <b>{lang}</b>ga o'zgartirildi.",
    },
}

# Supported learning/translation languages
LANGUAGE_META = {
    "en": {"flag": "🇬🇧", "name": "English"},
    "ru": {"flag": "🇷🇺", "name": "Русский"},
    "uz": {"flag": "🇺🇿", "name": "O'zbekcha"},
    "tr": {"flag": "🇹🇷", "name": "Türkçe"},
    "de": {"flag": "🇩🇪", "name": "Deutsch"},
    "fr": {"flag": "🇫🇷", "name": "Français"},
    "kk": {"flag": "🇰🇿", "name": "Қазақша"},
    "ar": {"flag": "🇦🇪", "name": "العربية"},
    "ko": {"flag": "🇰🇷", "name": "한국어"},
    "zh-CN": {"flag": "🇨🇳", "name": "中文"},
}

# Display names for interface languages
LANG_DISPLAY = {"en": "English", "ru": "Русский", "uz": "O'zbekcha"}
TARGET_LANG_DISPLAY = {code: data["name"] for code, data in LANGUAGE_META.items()}

# All known button texts across all locales (for filters)
def _collect_btn(key: str) -> list[str]:
    return list({MESSAGES[loc][key] for loc in MESSAGES if key in MESSAGES[loc]})

BTN_ADD_WORDS = _collect_btn("btn_add_words")
BTN_TRAIN = _collect_btn("btn_train")
BTN_LEARN_NEW = _collect_btn("btn_learn_new")
BTN_RESULTS = _collect_btn("btn_results")
BTN_VOCABULARY = _collect_btn("btn_vocabulary")
BTN_MY_WORDS = list({*BTN_VOCABULARY, *_collect_btn("btn_my_words")})
BTN_SETTINGS = _collect_btn("btn_settings")

DEFAULT_LOCALE = "en"
SUPPORTED_UI_LOCALES = {"en", "ru", "uz"}


def resolve_ui_locale(target_lang: str | None) -> str:
    """Map user's native language to UI locale, fallback to English."""
    if not target_lang:
        return DEFAULT_LOCALE
    return target_lang if target_lang in SUPPORTED_UI_LOCALES else DEFAULT_LOCALE


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


def get_flag(lang_code: str) -> str:
    """Return emoji flag for selected language."""
    return LANGUAGE_META.get(lang_code, LANGUAGE_META["en"])["flag"]


def get_language_name(lang_code: str) -> str:
    """Return display name for selected language."""
    return LANGUAGE_META.get(lang_code, LANGUAGE_META["en"])["name"]
