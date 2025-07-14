import logging
import random
import json
from datetime import datetime, time
from pytz import timezone
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = "ضع_التوكن_هنا"
ADMIN_ID = 1438736069
TIMEZONE = timezone("Africa/Cairo")

# البيانات
morning_azkar = ["أذكار الصباح 1", "أذكار الصباح 2"]
evening_azkar = ["أذكار المساء 1", "أذكار المساء 2"]
ayahs = ["وَقُل رَّبِّ زِدْنِي عِلْمًا", "إِنَّ مَعَ الْعُسْرِ يُسْرًا"]
duas = ["اللهم اجعل القرآن ربيع قلوبنا", "اللهم اجعلنا من الذاكرين"]
friday_reminders = ["🌙 لا تنسَ سورة الكهف", "🕌 صلّ على النبي 💌"]

images = [
    "https://i.imgur.com/abc1.jpg",
    "https://i.imgur.com/abc2.jpg",
    "https://i.imgur.com/abc3.jpg"
]

# الإعدادات الافتراضية
user_settings = {
    "morning_time": "08:00",
    "evening_time": "17:00"
}

# اللوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# جدولة
scheduler = BackgroundScheduler(timezone=TIMEZONE)

def send_with_image(context: CallbackContext, text: str):
    chat_id = context.job.context
    photo_url = random.choice(images)
    context.bot.send_photo(chat_id=chat_id, photo=photo_url, caption=text)

def send_morning(context: CallbackContext):
    text = f"🌅 {random.choice(morning_azkar)}"
    send_with_image(context, text)

def send_evening(context: CallbackContext):
    text = f"🌇 {random.choice(evening_azkar)}"
    send_with_image(context, text)

def send_ayah(context: CallbackContext):
    text = f"📖 آية:\n{random.choice(ayahs)}"
    send_with_image(context, text)

def send_dua(context: CallbackContext):
    text = f"🕊️ دعاء:\n{random.choice(duas)}"
    send_with_image(context, text)

def send_friday_reminder(context: CallbackContext):
    today = datetime.now(TIMEZONE).strftime("%A")
    if today == "Friday":
        text = f"🌟 تذكير الجمعة:\n{random.choice(friday_reminders)}"
        send_with_image(context, text)

# أوامر البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 أهلاً بك! استخدم /activate لتشغيل التذكيرات.")

def activate(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        morning_time = datetime.strptime(user_settings["morning_time"], "%H:%M").time()
        evening_time = datetime.strptime(user_settings["evening_time"], "%H:%M").time()

        scheduler.add_job(send_morning, 'cron', hour=morning_time.hour, minute=morning_time.minute, context=chat_id)
        scheduler.add_job(send_evening, 'cron', hour=evening_time.hour, minute=evening_time.minute, context=chat_id)
        scheduler.add_job(send_ayah, 'interval', hours=8, context=chat_id)
        scheduler.add_job(send_dua, 'interval', hours=12, context=chat_id)
        scheduler.add_job(send_friday_reminder, 'cron', day_of_week='fri', hour=9, context=chat_id)

        update.message.reply_text("✅ تم تفعيل التذكيرات.")
    except Exception as e:
        logger.error(f"[Activate Error]: {e}")
        update.message.reply_text("حدث خطأ أثناء التفعيل.")

def set_time(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ الأمر للمشرف فقط.")
        return

    try:
        part = context.args[0].lower()
        value = context.args[1]
        datetime.strptime(value, "%H:%M")  # تأكد من التنسيق
        if part == "morning":
            user_settings["morning_time"] = value
        elif part == "evening":
            user_settings["evening_time"] = value
        else:
            update.message.reply_text("استخدم: /settime morning 08:00 أو evening 18:00")
            return
        update.message.reply_text(f"⏰ تم تحديث توقيت {part} إلى {value}")
    except:
        update.message.reply_text("❌ خطأ في التنسيق. استخدم /settime morning 08:00")

def prayer(update: Update, context: CallbackContext):
    update.message.reply_text("🕌 مواقيت الصلاة:\nالفجر: 03:30\nالظهر: 12:00\nالعصر: 15:30\nالمغرب: 18:45\nالعشاء: 20:00")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activate", activate))
    dp.add_handler(CommandHandler("settime", set_time))
    dp.add_handler(CommandHandler("prayer", prayer))

    scheduler.start()
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
