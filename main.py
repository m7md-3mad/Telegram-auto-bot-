import json
import os
import requests
from datetime import datetime, time, timedelta
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

BOT_TOKEN = "7674655190:AAHGQbac6F9ecwtp7fP0DK5B3_38cs0Jv1M"
CHAT_ID = "-1002470716958"
SETTINGS_FILE = "settings.json"

default_settings = {
    "morning_time": "06:00",
    "evening_time": "18:00",
    "ayat_interval": 120,  # بالدقائق
    "dua_interval": 180,   # بالدقائق
    "prayer_alerts": True
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

def get_prayer_times():
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": "Alexandria",
        "country": "Egypt",
        "method": 5
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data["code"] == 200:
            return data["data"]["timings"]
        else:
            return None
    except Exception as e:
        print(f"Error getting prayer times: {e}")
        return None

def send_prayer_times(context: CallbackContext):
    timings = get_prayer_times()
    if timings:
        msg = "🕌 مواقيت الصلاة اليوم في الإسكندرية:\n"
        for prayer, t in timings.items():
            if prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                msg += f"{prayer}: {t}\n"
        send_message(context, msg)
    else:
        send_message(context, "❌ لم أتمكن من جلب مواقيت الصلاة اليوم.")

def send_prayer_alert(context: CallbackContext):
    job = context.job
    send_message(context, f"🕋 تذكير: الصلاة {job.name} ستبدأ بعد 5 دقائق، استعد!")

def schedule_prayer_alerts(job_queue):
    timings = get_prayer_times()
    if not timings:
        return
    # نصنع تنبيهات قبل الصلاة بـ5 دقائق
    prayer_names = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    for pname in prayer_names:
        prayer_time_str = timings[pname]
        prayer_time = datetime.strptime(prayer_time_str, "%H:%M").time()
        alert_time = (datetime.combine(datetime.today(), prayer_time) - timedelta(minutes=5)).time()

        # نتأكد التنبيه ما يكونش قبل الوقت الحالي
        now = datetime.now().time()
        if alert_time > now:
            job_queue.run_daily(send_prayer_alert, alert_time, name=pname)

def reschedule_jobs(job_queue):
    job_queue.scheduler.remove_all_jobs()

    job_queue.run_daily(send_morning, parse_time(settings["morning_time"]))
    job_queue.run_daily(send_evening, parse_time(settings["evening_time"]))

    job_queue.run_repeating(send_ayat, interval=settings["ayat_interval"]*60, first=10)
    job_queue.run_repeating(send_dua, interval=settings["dua_interval"]*60, first=20)

    if settings.get("prayer_alerts", True):
        # نرسل مواقيت الصلاة مرة في اليوم الصبح
        job_queue.run_daily(send_prayer_times, time(7,0))
        # نحدد التنبيهات قبل الصلاة
        schedule_prayer_alerts(job_queue)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "أهلاً! هذا بوت الأذكار.\n"
        "استخدم /activate لتشغيل الإرسال التلقائي.\n"
        "استخدم /deactivate لإيقاف الإرسال.\n"
        "استخدم /status لعرض الإعدادات الحالية."
    )

def activate(update: Update, context: CallbackContext):
    try:
        reschedule_jobs(context.job_queue)
        update.message.reply_text("✅ تم تفعيل الإرسال التلقائي.")
    except Exception as e:
        update.message.reply_text(f"حدث خطأ أثناء التفعيل: {e}")

def deactivate(update: Update, context: CallbackContext):
    context.job_queue.scheduler.remove_all_jobs()
    update.message.reply_text("⛔ تم إيقاف الإرسال التلقائي.")

def status(update: Update, context: CallbackContext):
    msg = (
        "🧾 الإعدادات الحالية:\n"
        f"🌅 أذكار الصباح: {settings.get('morning_time')}\n"
        f"🌙 أذكار المساء: {settings.get('evening_time')}\n"
        f"📖 آية كل: {settings.get('ayat_interval')} دقيقة\n"
        f"🤲 دعاء كل: {settings.get('dua_interval')} دقيقة\n"
        f"🕌 تنبيهات الصلاة: {'مفعلة' if settings.get('prayer_alerts', True) else 'معطلة'}"
    )
    update.message.reply_text(msg)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activate", activate))
    dp.add_handler(CommandHandler("deactivate", deactivate))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
