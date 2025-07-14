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

# آي دي القناة
CHAT_ID = "-1002470716958"

# أذكار الصباح
MORNING_AZKAR = """
📿 أذكار الصباح:

1. بِسـمِ اللهِ الذي لا يَضُـرُّ مَعَ اسمِـهِ شَيءٌ في الأرْضِ وَلا في السّمـاءِ وَهـوَ السّمـيعُ العَلـيم. ×3
2. رَضيـتُ بِاللهِ رَبَّـاً وَبِالإسْلامِ ديـناً وَبِمُحَـمَّدٍ صلى الله عليه وسلم نَبِيّـاً.  ×3
3. سُبْحـانَ اللهِ وَبِحَمْـدِهِ عَدَدَ خَلْـقِه ، وَرِضـا نَفْسِـه ، وَزِنَـةَ عَـرْشِـه ، وَمِـدادَ كَلِمـاتِـه.
4. اللّهُـمَّ إِنِّـي أَصْبَـحْتُ أُشْـهِدُك ، وَأُشْـهِدُ حَمَلَـةَ عَـرْشِـك ، وَمَلَائِكَتَكَ ، وَجَمـيعَ خَلْـقِك ، أَنَّـكَ أَنْـتَ اللهُ لا إلهَ إلاّ أَنْـتَ وَحْـدَكَ لا شَريكَ لَـك ، وَأَنَّ مُحَمّـداً عَبْـدُكَ وَرَسـولُـك.
"""

# أذكار المساء
EVENING_AZKAR = """
📿 أذكار المساء:

1. رَضيـتُ بِاللهِ رَبَّـاً وَبِالإسْلامِ ديـناً وَبِمُحَـمَّدٍ صلى الله عليه وسلم نَبِيّـاً و رسولا . ×3
2. اللّهُـمَّ ما أَمسى بي مِـنْ نِعْـمَةٍ أَو بِأَحَـدٍ مِـنْ خَلْـقِك ، فَمِـنْكَ وَحْـدَكَ لا شريكَ لَـك ، فَلَـكَ الْحَمْـدُ وَلَـكَ الشُّكْـر.
3. يَا حَيُّ يَا قيُّومُ بِرَحْمَتِكَ أسْتَغِيثُ أصْلِحْ لِي شَأنِي كُلَّهُ وَلاَ تَكِلْنِي إلَى نَفْسِي طَـرْفَةَ عَيْنٍ.
4. اللّهُـمَّ عافِـني في بَدَنـي ، اللّهُـمَّ عافِـني في سَمْـعي ، اللّهُـمَّ عافِـني في بَصَـري ، لا إلهَ إلاّ أَنْـتَ.
5. أَعـوذُ بِكَلِمـاتِ اللّهِ التّـامّـاتِ مِنْ شَـرِّ ما خَلَـق.
"""

# أذكار الجمعة
FRIDAY_REMINDER = """
🔹🔸يوم الجمعة🔸🔹

﴿ يا أَيُّهَا الَّذِينَ آمَنُوا إِذَا نُودِيَ لِلصَّلَاةِ مِنْ يَوْمِ الْجُمُعَةِ فَاسْعَوْا إِلَى ذِكْرِ اللَّهِ وَذَرُوا الْبَيْعَ ﴾ [الجمعة:9]

قال رسول الله ﷺ:
(خَيْرُ يَوْمٍ طَلَعَتْ عَلَيْهِ الشَّمْسُ يَوْمُ الْجُمُعَةِ...)

**سنن الجمعة:**
1- الاغتسال
2- التطيب
3- التبكير إلى المسجد
4- تحرى ساعة الإجابة
5- لبس أحسن الثياب
6- كثرة الصلاة على النبي ﷺ
7- قراءة سورة الكهف
8- التسوك
"""

def send_message(context: CallbackContext, message: str):
    context.bot.send_message(chat_id=CHAT_ID, text=message)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("📿 تم تفعيل إرسال الأذكار التلقائي.")

def send_morning(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=MORNING_AZKAR)

def send_evening(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=EVENING_AZKAR)

def send_friday(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=FRIDAY_REMINDER)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("morning", send_morning))
    dp.add_handler(CommandHandler("evening", send_evening))
    dp.add_handler(CommandHandler("friday", send_friday))

    tz = pytz.timezone("Africa/Cairo")
    scheduler = BackgroundScheduler(timezone=tz)
    scheduler.add_job(send_message, 'cron', hour=4, minute=25, args=[updater.bot, MORNING_AZKAR])
    scheduler.add_job(send_message, 'cron', hour=20, minute=6, args=[updater.bot, EVENING_AZKAR])
    scheduler.add_job(send_message, 'cron', day_of_week='fri', hour=7, minute=0, args=[updater.bot, FRIDAY_REMINDER])
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
