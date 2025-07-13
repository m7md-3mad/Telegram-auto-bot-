import json
import os
from datetime import time as dt_time
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "7674655190:AAEUxpXd5P-Z-SEzmo7qKnxXlyhnG9JcVqg"
CHAT_ID = "-1002470716958"
SETTINGS_FILE = "settings.json"

default_settings = {
    "morning_time": "06:00",
    "evening_time": "18:00",
    "ayat_interval": 120,
    "dua_interval": 180
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        return default_settings.copy()

settings = load_settings()

def start(update, context):
    update.message.reply_text(
        "أهلاً! هذا بوت الأذكار.\n"
        "استخدم /activate لتشغيل الإرسال التلقائي.\n"
        "استخدم /status لعرض الإعدادات الحالية."
    )

def activate(update, context):
    update.message.reply_text("✅ تم تفعيل الإرسال التلقائي (تجريبي فقط).")

def status(update, context):
    msg = (
        "🧾 الإعدادات الحالية:\n"
        f"أذكار الصباح: {settings.get('morning_time')}\n"
        f"أذكار المساء: {settings.get('evening_time')}\n"
        f"آيات كل: {settings.get('ayat_interval')} دقيقة\n"
        f"أدعية كل: {settings.get('dua_interval')} دقيقة"
    )
    update.message.reply_text(msg)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activate", activate))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
