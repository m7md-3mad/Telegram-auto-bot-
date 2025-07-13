import json
import os
import random
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = "ضع_توكن_البوت_هنا"
CHAT_ID = "-1002470716958"
ADMIN_ID = 1438736069
SETTINGS_FILE = "settings.json"

images = [
    "https://i.imgur.com/9QZf5Qb.jpeg",
    "https://i.imgur.com/CQ5ELcC.jpeg",
    "https://i.imgur.com/w1u45Bb.jpeg",
    "https://i.imgur.com/rMBRfaM.jpeg",
]

default_settings = {
    "morning_time": "06:00",
    "evening_time": "18:00",
    "friday_reminder_time": "11:00",
    "ayat_interval": 180,
    "dua_interval": 240
}

morning_azkar = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "اللَّهُمَّ أَجِرْنِي مِنَ النَّارِ"]
evening_azkar = ["اللّهُـمَّ أَنْتَ رَبِّي لا إِلَهَ إِلَّا أَنْتَ", "أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ"]
ayat = ["وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ", "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ"]
duaas = ["اللهم إني أسألك العفو والعافية", "اللهم اجعلني من التوابين"]

timezone = pytz.timezone("Africa/Cairo")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, ensure_ascii=False)
        return default_settings

settings = load_settings()
scheduler = BackgroundScheduler(timezone=timezone)

def send_with_image(context: CallbackContext, text: str):
    img = random.choice(images)
    context.bot.send_photo(chat_id=CHAT_ID, photo=img, caption=text)

def send_morning(context: CallbackContext):
    for z in morning_azkar:
        send_with_image(context, f"🌅 {z}")

def send_evening(context: CallbackContext):
    for z in evening_azkar:
        send_with_image(context, f"🌙 {z}")

def send_friday(context: CallbackContext):
    if datetime.now(timezone).weekday() == 4:
        send_with_image(context, "📿 لا تنسَ سورة الكهف والصلاة على النبي ﷺ")

def send_ayat(context: CallbackContext):
    verse = random.choice(ayat)
    send_with_image(context, f"📖 آية:\n{verse}")

def send_duaa(context: CallbackContext):
    dua = random.choice(duaas)
    send_with_image(context, f"🤲 دعاء:\n{dua}")

def reschedule_jobs(updater):
    scheduler.remove_all_jobs()
    
    h, m = map(int, settings["morning_time"].split(":"))
    scheduler.add_job(send_morning, 'cron', hour=h, minute=m, args=[updater.bot])

    h, m = map(int, settings["evening_time"].split(":"))
    scheduler.add_job(send_evening, 'cron', hour=h, minute=m, args=[updater.bot])

    h, m = map(int, settings["friday_reminder_time"].split(":"))
    scheduler.add_job(send_friday, 'cron', day_of_week='fri', hour=h, minute=m, args=[updater.bot])

    scheduler.add_job(send_ayat, 'interval', minutes=settings["ayat_interval"], args=[updater.bot], next_run_time=datetime.now())
    scheduler.add_job(send_duaa, 'interval', minutes=settings["dua_interval"], args=[updater.bot], next_run_time=datetime.now())

def start(update: Update, context: CallbackContext):
    update.message.reply_text("أهلاً بك في بوت الأذكار. استخدم /settime أو /duaa أو /verse")

def duaa(update: Update, context: CallbackContext):
    send_duaa(context)

def verse(update: Update, context: CallbackContext):
    send_ayat(context)

def settime(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ غير مصرح لك باستخدام هذا الأمر.")
        return

    try:
        args = context.args
        if len(args) != 2:
            raise ValueError

        settings["morning_time"] = args[0]
        settings["evening_time"] = args[1]
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False)

        reschedule_jobs(context.bot)
        update.message.reply_text("✅ تم تحديث التوقيتات بنجاح.")
    except:
        update.message.reply_text("❌ صيغة الأمر خاطئة. استخدم مثلًا:\n/settime 06:00 18:00")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("settime", settime))
    dp.add_handler(CommandHandler("duaa", duaa))
    dp.add_handler(CommandHandler("verse", verse))

    scheduler.start()
    reschedule_jobs(updater)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
