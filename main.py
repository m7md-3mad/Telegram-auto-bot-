import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# إعداد اللوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# توكن البوت
BOT_TOKEN = "7674655190:AAGuHfCmf3VX0qFXqUZi4eZOEgos_UnjjKY"

# آي دي القناة أو المستخدم
CHAT_ID = "-1002470716958"  # غيّر هذا إن لزم

# أذكار تجريبية
TEST_DHIKR = "🔁 هذا ذكر تجريبي يتم إرساله كل دقيقة للتأكد من عمل الجدولة."

def send_message(context: CallbackContext, message: str):
    context.bot.send_message(chat_id=CHAT_ID, text=message)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("📿 تم تفعيل إرسال الذكر التجريبي كل دقيقة.")

def send_test_dhikr(context: CallbackContext):
    send_message(context, TEST_DHIKR)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # أوامر
    dp.add_handler(CommandHandler("start", start))

    # إعداد التوقيت
    tz = pytz.timezone("Africa/Cairo")
    scheduler = BackgroundScheduler(timezone=tz)

    # ذكر كل دقيقة
    scheduler.add_job(send_test_dhikr, 'interval', minutes=1)

    scheduler.start()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
