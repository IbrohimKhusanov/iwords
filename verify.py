#!/usr/bin/env python3
"""Quick verification script for multi-language support."""
import sys
sys.path.insert(0, '.')

try:
    from i18n import t, get_flag
    print("✅ i18n OK")

    from database.models import User, Word
    print(f"✅ User columns: {[c.name for c in User.__table__.columns]}")
    print(f"✅ Word columns: {[c.name for c in Word.__table__.columns]}")

    from keyboards.main import main_menu_kb
    from keyboards.inline import language_kb, settings_kb
    print("✅ Keyboards OK")

    from handlers import start, add_word, new_words, training
    print("✅ Handlers OK")

    from middlewares.db import DbSessionMiddleware
    print("✅ Middleware OK")

    from services.translator import translate_word
    print("✅ Translator OK")

    print("\n🎉 All modules verified successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
