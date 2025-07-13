import json
import os
from datetime import time, datetime
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

BOT_TOKEN = "7674655190:AAHGQbac6F9ecwtp7fP0DK5B3_38cs0Jv1M"
CHAT_ID = "-1002470716958"

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
    "📖 ﴿وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ﴾",
    "📖 ﴿اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ﴾",
    "📖 ﴿وَمَا تَوْفِيقِي إِلَّا بِاللَّهِ﴾"
]

dua_list = [
    "🤲 اللهم إني أسألك العفو والعافية في الدنيا والآخرة",
    "🤲 اللهم اجعلني من التوابين واجعلني من المتطهرين",
    "🤲 اللهم ارحمني واغفر لي وارزقني الخير حيثما كنت"
]

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
    for z in morning_azkar:
        send_message(context, z)

def send_evening(context: CallbackContext):
    for z in evening_azkar:
        send_message(context, z)

def send_ayat(context: CallbackContext):
    ayat = ayat_list[datetime.now().minute % len(ayat_list)]
    send_message(context, ayat)

def send_dua(context: CallbackContext):
    dua = dua_list[datetime.now().minute % len(dua_list)]
    send_message(context, dua)

def reschedule_jobs(job_queue):
    job_queue.scheduler.remove_all_jobs()
    job_queue.run_daily(send_morning, parse_time(settings["morning_time"]))
    job_queue.run_daily(send_evening, parse_time(settings["evening_time"]))
    job_queue.run_repeating(send_ayat, interval=settings["ayat_interval"] * 60, first=10)
    job_queue.run_repeating(send_dua, interval=settings["dua_interval"] * 60, first=20)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 أهلاً بك في بوت الأذكار.\n"
        "/activate لتشغيل الإرسال التلقائي\n"
        "/deactivate لإيقافه\n"
        "/status لعرض الإعدادات\n"
        "/set_morning HH:MM لتعديل وقت الصباح\n"
        "/set_evening HH:MM لتعديل وقت المساء\n"
        "/set_ayat_interval عدد_دقائق لتغيير معدل الآيات\n"
        "/set_dua_interval عدد_دقائق لتغيير معدل الأدعية"
    )

def activate(update: Update, context: CallbackContext):
    try:
        reschedule_jobs(context.job_queue)
        update.message.reply_text("✅ تم تفعيل الإرسال التلقائي.")
    except Exception as e:
        update.message.reply_text(f"❌ حدث خطأ أثناء التفعيل: {e}")

def deactivate(update: Update, context: CallbackContext):
    context.job_queue.scheduler.remove_all_jobs()
    update.message.reply_text("⛔ تم إيقاف الإرسال التلقائي.")

def status(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"🌅 الصباح: {settings['morning_time']}\n"
        f"🌙 المساء: {settings['evening_time']}\n"
        f"📖 آية كل: {settings['ayat_interval']} دقيقة\n"
        f"🤲 دعاء كل: {settings['dua_interval']} دقيقة"
    )

def set_morning(update: Update, context: CallbackContext):
    if context.args:
        settings["morning_time"] = context.args[0]
        save_settings(settings)
        update.message.reply_text(f"✅ تم تحديث وقت الصباح إلى {context.args[0]}.")

def set_evening(update: Update, context: CallbackContext):
    if context.args:
        settings["evening_time"] = context.args[0]
        save_settings(settings)
        update.message.reply_text(f"✅ تم تحديث وقت المساء إلى {context.args[0]}.")

def set_ayat_interval(update: Update, context: CallbackContext):
    if context.args:
        settings["ayat_interval"] = int(context.args[0])
        save_settings(settings)
        update.message.reply_text(f"✅ تم تحديث معدل إرسال الآيات إلى {context.args[0]} دقيقة.")

def set_dua_interval(update: Update, context: CallbackContext):
    if context.args:
        settings["dua_interval"] = int(context.args[0])
        save_settings(settings)
        update.message.reply_text(f"✅ تم تحديث معدل إرسال الأدعية إلى {context.args[0]} دقيقة.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activate", activate))
    dp.add_handler(CommandHandler("deactivate", deactivate))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("set_morning", set_morning))
    dp.add_handler(CommandHandler("set_evening", set_evening))
    dp.add_handler(CommandHandler("set_ayat_interval", set_ayat_interval))
    dp.add_handler(CommandHandler("set_dua_interval", set_dua_interval))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
