# 📚 iWords — Telegram Vocabulary Bot

A personal vocabulary trainer bot for Telegram with spaced repetition (SRS),
automatic translation via Google Translate, and support for any language pair.

---

## ✨ Features

- 🌐 **Universal language pairs** — learn any language, translate to any language
- 🎯 **Spaced repetition (SRS)** — Anki-style intervals: 1 → 3 → 7 → 14 → 30 days
- 📝 **Two practice modes** — translation recall or sentence completion
- 🔤 **Auto translation** — powered by Google Translate
- 📖 **Batch import** — add up to 150 words at once
- 📊 **Progress tracking** — see new / learning / learned stats
- 🗂 **Vocabulary browser** — paginated word list
- 🌍 **3 interface languages** — English, Russian, Uzbek

---

## 🌍 Supported Languages

| Flag | Language  | Code |
|------|-----------|------|
| 🇬🇧 | English   | `en` |
| 🇷🇺 | Russian   | `ru` |
| 🇺🇿 | Uzbek     | `uz` |
| 🇹🇷 | Turkish   | `tr` |
| 🇩🇪 | German    | `de` |
| 🇫🇷 | French    | `fr` |
| 🇰🇿 | Kazakh    | `kk` |
| 🇦🇪 | Arabic    | `ar` |
| 🇰🇷 | Korean    | `ko` |
| 🇨🇳 | Chinese   | `zh` |

Any combination works — for example:
- 🇺🇿 Uzbek speaker learning 🇹🇷 Turkish
- 🇷🇺 Russian speaker learning 🇩🇪 German
- 🇬🇧 English speaker learning 🇰🇷 Korean

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/IbrohimKhusanov/iwords.git
cd iwords
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

### 4. Run the bot

```bash
python bot.py
```

The database (`words.db`) is created automatically on first launch.


