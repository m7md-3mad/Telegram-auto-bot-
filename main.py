import json
import os
from datetime import time, datetime
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

BOT_TOKEN = "ضع_توكن_البوت_هنا"
CHAT_ID = "-1002470716958"  # ID القناة أو الجروب
SETTINGS_FILE = "settings.json"

default_settings = {
    "morning_time": "06:00",
    "evening_time": "18:00",
    "ayat_interval": 120,
    "dua_interval": 180
}

morning_azkar = [
    "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ",
    "سُبْحَانَ اللَّهِ الْعَظِيمِ",
    "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ",
    "لا حَوْلَ وَلا قُوَّةَ إِلَّا بِاللَّهِ"
]

evening_azkar = [
    "اللّهُـمَّ أَنْتَ رَبِّي لا إِلَهَ إِلَّا أَنْتَ",
    "خَلَقْتَنِي وَأَنَا عَبْدُكَ",
    "وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ",
    "أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ"
]

ayat_list = [
    "وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ (68)",
    "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ (255)",
    "وَمَا تَوْفِيقِي إِلَّا بِاللَّهِ (29)",
]

dua_list = [
    "اللهم إني أسألك العفو والعافية في الدنيا والآخرة",
    "اللهم اجعلني من التوابين واجعلني من المتطهرين",
    "اللهم ارحمني واغفر لي وارزقني الخير حيثما كنت"
]

prayer_times = {
    "الفجر": "03:42 ص",
    "الظهر": "12:05 م",
    "العصر": "03:45 م",
    "المغرب": "06:58 م",
    "العشاء": "08:27 م"
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=4)
        return default_settings.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

settings = load_settings()

def parse_time(tstr):
    h, m = map(int, tstr.split(":"))
    return time(h, m)

def send_message(context: CallbackContext, text):
    context.bot.send_message(chat_id=CHAT_ID, text=text)

def send_morning(context: CallbackContext):
    for azkar in morning_azkar:
        send_message(context, azkar)

def send_evening(context: CallbackContext):
    for azkar in evening_azkar:
        send_message(context, azkar)

def send_ayat(context: CallbackContext):
    ayat = ayat_list[datetime.now().minute % len(ayat_list)]
    send_message(context, f"📖 آية:\n{ayat}")

def send_dua(context: CallbackContext):
    dua = dua_list[datetime.now().minute % len(dua_list)]
    send_message(context, f"🤲 دعاء:\n{dua}")

def reschedule_jobs(job_queue):
    job_queue.scheduler.remove_all_jobs()

    job_queue.run_daily(send_morning, parse_time(settings["morning_time"]))
    job_queue.run_daily(send_evening, parse_time(settings["evening_time"]))
    job_queue.run_repeating(send_ayat, interval=settings["ayat_interval"]*60, first=10)
    job_queue.run_repeating(send_dua, interval=settings["dua_interval"]*60, first=20)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 مرحبًا بك في بوت الأذكار.\n"
        "استخدم /activate لتشغيل الإرسال التلقائي.\n"
        "استخدم /deactivate لإيقاف الإرسال.\n"
        "استخدم /status لعرض الإعدادات.\n"
        "استخدم /settime لتغيير التوقيتات.\n"
        "استخدم /prayer لعرض مواقيت الصلاة."
    )

def activate(update: Update, context: CallbackContext):
    try:
        reschedule_jobs(context.job_queue)
        update.message.reply_text("✅ تم تفعيل الإرسال التلقائي.")
    except Exception as e:
        update.message.reply_text(f"[Activate Error]: {e}")

def deactivate(update: Update, context: CallbackContext):
    context.job_queue.scheduler.remove_all_jobs()
    update.message.reply_text("⛔ تم إيقاف الإرسال التلقائي.")

def status(update: Update, context: CallbackContext):
    msg = (
        "🧾 الإعدادات الحالية:\n"
        f"🌅 أذكار الصباح: {settings.get('morning_time')}\n"
        f"🌙 أذكار المساء: {settings.get('evening_time')}\n"
        f"📖 آية كل: {settings.get('ayat_interval')} دقيقة\n"
        f"🤲 دعاء كل: {settings.get('dua_interval')} دقيقة"
    )
    update.message.reply_text(msg)

def set_time(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        update.message.reply_text("❌ الصيغة:\n/settime [النوع] [القيمة]\nمثال: /settime morning 06:30")
        return

    setting_type = context.args[0]
    value = context.args[1]

    valid_keys = {
        "morning": "morning_time",
        "evening": "evening_time",
        "ayah": "ayat_interval",
        "dua": "dua_interval"
    }

    if setting_type not in valid_keys:
        update.message.reply_text("❌ الأنواع المتاحة: morning, evening, ayah, dua")
        return

    key = valid_keys[setting_type]

    try:
        if "time" in key:
            datetime.strptime(value, "%H:%M")
        else:
            value = int(value)
    except:
        update.message.reply_text("❌ قيمة غير صحيحة.")
        return

    settings[key] = value
    save_settings(settings)
    reschedule_jobs(context.job_queue)

    update.message.reply_text(f"✅ تم تحديث {setting_type} إلى {value}")

def prayer(update: Update, context: CallbackContext):
    msg = "🕌 مواقيت الصلاة في الإسكندرية:\n\n"
    for name, time_ in prayer_times.items():
        msg += f"{name}: {time_}\n"
    update.message.reply_text(msg)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activate", activate))
    dp.add_handler(CommandHandler("deactivate", deactivate))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("settime", set_time))
    dp.add_handler(CommandHandler("prayer", prayer))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
