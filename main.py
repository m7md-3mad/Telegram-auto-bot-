import random
import json
import os
from datetime import time as dt_time
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = "7674655190:AAEUxpXd5P-Z-SEzmo7qKnxXlyhnG9JcVqg"
CHAT_ID = "-1002470716958"
SETTINGS_FILE = "settings.json"

# محتوى الأذكار
morning_azkar = "🌅 أذكار الصباح 🌅\nاللّهُ لا إلهَ إلا هو الحيُّ القيومُ..."
evening_azkar = "🌙 أذكار المساء 🌙\nأعوذُ بكلماتِ اللهِ التاماتِ من شرِّ ما خلق."
ayat_list = [
    "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ",
    "إِنَّ اللّهَ مَعَ الصَّابِرِينَ",
    "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا"
]
duas_list = [
    "اللهم اجعلني من الذين يستمعون القول فيتبعون أحسنه.",
    "اللهم ارزقني حبك، وحب من يحبك، وحب عمل يقربني إلى حبك.",
]

# الإعدادات الافتراضية
default_settings = {
    "morning_time": "06:00",
    "evening_time": "18:00",
    "ayat_interval": 120,
    "dua_interval": 180
}

# تحميل أو إنشاء الإعدادات
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        return default_settings.copy()

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

settings = load_settings()

# تحويل الوقت من سترنج إلى كائن وقت
def parse_time(tstr):
    h, m = map(int, tstr.split(":"))
    return dt_time(hour=h, minute=m)

# وظائف الإرسال
def send_morning(context: CallbackContext):
    context.bot.send_message(chat_id=CHAT_ID, text=morning_azkar)

def send_evening(context: CallbackContext):
    context.bot.send_message(chat_id=CHAT_ID, text=evening_azkar)

def send_ayat_periodic(context: CallbackContext):
    context.bot.send_message(chat_id=CHAT_ID, text="📖 " + random.choice(ayat_list))

def send_dua_periodic(context: CallbackContext):
    context.bot.send_message(chat_id=CHAT_ID, text="🤲 " + random.choice(duas_list))

# إعادة جدولة المهام
def reschedule_jobs(job_queue):
    job_queue.scheduler.remove_all_jobs()
    job_queue.run_daily(send_morning, time=parse_time(settings["morning_time"]))
    job_queue.run_daily(send_evening, time=parse_time(settings["evening_time"]))
    job_queue.run_repeating(send_ayat_periodic, interval=int(settings["ayat_interval"]) * 60, first=0)
    job_queue.run_repeating(send_dua_periodic, interval=int(settings["dua_interval"]) * 60, first=0)

# أوامر البوت
def start(update, context):
    update.message.reply_text(
        "السلام عليكم! 🌿\n"
        "أوامر التحكم:\n"
        "/activate - تشغيل الإرسال التلقائي\n"
        "/stop - إيقاف الإرسال\n"
        "/status - عرض الإعدادات الحالية\n"
        "/set_morning HH:MM - تعديل وقت أذكار الصباح\n"
        "/set_evening HH:MM - تعديل وقت أذكار المساء\n"
        "/set_ayat دقائق - تحديد تكرار الآيات\n"
        "/set_dua دقائق - تحديد تكرار الأدعية"
    )

def activate(update, context):
    reschedule_jobs(context.job_queue)
    update.message.reply_text("✅ تم تفعيل الإرسال التلقائي.")

def stop(update, context):
    context.job_queue.scheduler.remove_all_jobs()
    update.message.reply_text("⛔ تم إيقاف الإرسال التلقائي.")

def ayat(update, context):
    update.message.reply_text("📖 " + ayat_list[0])

def ayat_random(update, context):
    update.message.reply_text("📖 " + random.choice(ayat_list))

def dua(update, context):
    update.message.reply_text("🤲 " + random.choice(duas_list))

def set_morning(update, context):
    try:
        time_str = context.args[0]
        parse_time(time_str)  # Validate
        settings["morning_time"] = time_str
        save_settings()
        reschedule_jobs(context.job_queue)
        update.message.reply_text(f"🌅 تم ضبط أذكار الصباح على {time_str}")
    except:
        update.message.reply_text("❌ استخدم الصيغة: /set_morning HH:MM")

def set_evening(update, context):
    try:
        time_str = context.args[0]
        parse_time(time_str)
        settings["evening_time"] = time_str
        save_settings()
        reschedule_jobs(context.job_queue)
        update.message.reply_text(f"🌙 تم ضبط أذكار المساء على {time_str}")
    except:
        update.message.reply_text("❌ استخدم الصيغة: /set_evening HH:MM")

def set_ayat(update, context):
    try:
        minutes = int(context.args[0])
        settings["ayat_interval"] = minutes
        save_settings()
        reschedule_jobs(context.job_queue)
        update.message.reply_text(f"📖 سيتم إرسال آية كل {minutes} دقيقة.")
    except:
        update.message.reply_text("❌ استخدم: /set_ayat عدد_الدقائق")

def set_dua(update, context):
    try:
        minutes = int(context.args[0])
        settings["dua_interval"] = minutes
        save_settings()
        reschedule_jobs(context.job_queue)
        update.message.reply_text(f"🤲 سيتم إرسال دعاء كل {minutes} دقيقة.")
    except:
        update.message.reply_text("❌ استخدم: /set_dua عدد_الدقائق")

def status(update, context):
    msg = (
        "🧾 *الإعدادات الحالية:*\n"
        f"🌅 أذكار الصباح: {settings['morning_time']}\n"
        f"🌙 أذكار المساء: {settings['evening_time']}\n"
        f"📖 آية كل: {settings['ayat_interval']} دقيقة\n"
        f"🤲 دعاء كل: {settings['dua_interval']} دقيقة"
    )
    update.message.reply_text(msg, parse_mode="Markdown")

# تشغيل البوت
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activate", activate))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("ayat", ayat))
    dp.add_handler(CommandHandler("ayatrandom", ayat_random))
    dp.add_handler(CommandHandler("dua", dua))
    dp.add_handler(CommandHandler("set_morning", set_morning, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("set_evening", set_evening, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("set_ayat", set_ayat, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("set_dua", set_dua, pass_args=True, pass_job_queue=True))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
