from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import logging

BOT_TOKEN = "7674655190:AAGuHfCmf3VX0qFXqUZi4eZOEgos_UnjjKY"
CHAT_ID = "-1002470716958"

# لوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_test_dhikr():
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text="🔁 هذا ذكر تجريبي يتم إرساله كل دقيقة للتجربة.")

def main():
    tz = pytz.timezone("Africa/Cairo")
    scheduler = BackgroundScheduler(timezone=tz)

    # إرسال الذكر كل دقيقة
    scheduler.add_job(send_test_dhikr, 'interval', minutes=1)

    scheduler.start()

    logger.info("⏳ البوت شغّال..")
    # منع توقف السكربت
    import time
    while True:
        time.sleep(60)

if __name__ == '__main__':
    main()
