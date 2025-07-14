import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# إعداد اللوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# التوكن والشات آي دي
BOT_TOKEN = "7674655190:AAGuHfCmf3VX0qFXqUZi4eZOEgos_UnjjKY"
CHAT_ID = "-1002470716958"

# الأذكار
MORNING_AZKAR = """📿 أذكار الصباح:
1. بِسـمِ اللهِ الذي لا يَضُـرُّ مَعَ اسمِـهِ شَيءٌ في الأرْضِ وَلا في السّمـاءِ وَهـوَ السّمـيعُ العَلـيم. ×3
2. رَضيـتُ بِاللهِ رَبَّـاً وَبِالإسْلامِ ديـناً وَبِمُحَـمَّدٍ صلى الله عليه وسلم نَبِيّـاً.  ×3
3. سُبْحـانَ اللهِ وَبِحَمْـدِهِ عَدَدَ خَلْـقِه ، وَرِضـا نَفْسِـه ، وَزِنَـةَ عَـرْشِـه ، وَمِـدادَ كَلِمـاتِـه.
4. اللّهُـمَّ إِنِّـي أَصْبَـحْتُ أُشْـهِدُك ... (إكمال الدعاء)
"""

EVENING_AZKAR = """📿 أذكار المساء:
1. رَضيـتُ بِاللهِ رَبَّـاً وَبِالإسْلامِ ديـناً ... ×3
2. اللّهُـمَّ ما أَمسى بي مِـنْ نِعْـمَةٍ ...
"""

FRIDAY_REMINDER = """🔹🔸يوم الجمعة🔸🔹
﴿ يا أَيُّهَا الَّذِينَ آمَنُوا إِذَا نُودِيَ لِلصَّلَاةِ ... ﴾
قال رسول الله ﷺ: (خَيْرُ يَوْمٍ ...)
**سنن الجمعة:**
1- الاغتسال ... إلخ
"""

# دوال الإرسال
def send_text(bot: Bot, message: str):
    bot.send_message(chat_id=CHAT_ID, text=message)

# أوامر البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text("📿 تم تفعيل إرسال الأذكار التلقائي.")

def send_morning(update: Update, context: CallbackContext):
    update.message.reply_text(MORNING_AZKAR)

def send_evening(update: Update, context: CallbackContext):
    update.message.reply_text(EVENING_AZKAR)

def send_friday(update: Update, context: CallbackContext):
    update.message.reply_text(FRIDAY_REMINDER)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # إضافة الكوماندز
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("morning", send_morning))
    dp.add_handler(CommandHandler("evening", send_evening))
    dp.add_handler(CommandHandler("friday", send_friday))

    # الجدولة
    tz = pytz.timezone("Africa/Cairo")
    scheduler = BackgroundScheduler(timezone=tz)
    scheduler.add_job(send_text, 'cron', hour=4, minute=25, args=[updater.bot, MORNING_AZKAR])
    scheduler.add_job(send_text, 'cron', hour=20, minute=6, args=[updater.bot, EVENING_AZKAR])
    scheduler.add_job(send_text, 'cron', day_of_week='fri', hour=7, minute=0, args=[updater.bot, FRIDAY_REMINDER])
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
