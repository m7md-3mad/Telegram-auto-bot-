import logging
from telegram import Update, BotCommand
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

# إعداد اللوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# توكن البوت
BOT_TOKEN = "7674655190:AAHGQbac6F9ecwtp7fP0DK5B3_38cs0Jv1M"

# نصوص الأذكار
MORNING_AZKAR = """
📿 أذكار الصباح:

1. بِسـمِ اللهِ الذي لا يَضُـرُّ مَعَ اسمِـهِ شَيءٌ في الأرْضِ وَلا في السّمـاءِ وَهـوَ السّمـيعُ العَلـيم. ×3
2. رَضيـتُ بِاللهِ رَبَّـاً وَبِالإسْلامِ ديـناً وَبِمُحَـمَّدٍ صلى الله عليه وسلم نَبِيّـاً.  ×3
3. سُبْحـانَ اللهِ وَبِحَمْـدِهِ عَدَدَ خَلْـقِه ، وَرِضـا نَفْسِـه ، وَزِنَـةَ عَـرْشِـه ، وَمِـدادَ كَلِمـاتِـه.
4. اللّهُـمَّ إِنِّـي أَصْبَـحْتُ أُشْـهِدُك ، وَأُشْـهِدُ حَمَلَـةَ عَـرْشِـك ، وَمَلَائِكَتَكَ ، وَجَمـيعَ خَلْـقِك ، أَنَّـكَ أَنْـتَ اللهُ لا إلهَ إلاّ أَنْـتَ وَحْـدَكَ لا شَريكَ لَـك ، وَأَنَّ مُحَمّـداً عَبْـدُكَ وَرَسـولُـك.
"""

EVENING_AZKAR = """
📿 أذكار المساء:

1. رَضيـتُ بِاللهِ رَبَّـاً وَبِالإسْلامِ ديـناً وَبِمُحَـمَّدٍ صلى الله عليه وسلم نَبِيّـاً و رسولا . ×3
2. اللّهُـمَّ ما أَمسى بي مِـنْ نِعْـمَةٍ أَو بِأَحَـدٍ مِـنْ خَلْـقِك ، فَمِـنْكَ وَحْـدَكَ لا شريكَ لَـك ، فَلَـكَ الْحَمْـدُ وَلَـكَ الشُّكْـر.
3. يَا حَيُّ يَا قيُّومُ بِرَحْمَتِكَ أسْتَغِيثُ أصْلِحْ لِي شَأنِي كُلَّهُ وَلاَ تَكِلْنِي إلَى نَفْسِي طَـرْفَةَ عَيْنٍ.
4. اللّهُـمَّ عافِـني في بَدَنـي ، اللّهُـمَّ عافِـني في سَمْـعي ، اللّهُـمَّ عافِـني في بَصَـري ، لا إلهَ إلاّ أَنْـتَ.
5. أَعـوذُ بِكَلِمـاتِ اللّهِ التّـامّـاتِ مِنْ شَـرِّ ما خَلَـق.
"""

FRIDAY_AZKAR = """
🔹🔸يوم الجمعة🔸🔹
﴿ يا أَيُّهَا الَّذِينَ آمَنُوا إِذَا نُودِيَ لِلصَّلَاةِ مِنْ يَوْمِ الْجُمُعَةِ فَاسْعَوْا إِلَى ذِكْرِ اللَّهِ وَذَرُوا الْبَيْعَ ذَلِكُمْ خَيْرٌ لَكُمْ إِنْ كُنْتُمْ تَعْلَمُونَ ﴾ [الجمعة:9]

قال رسول الله ﷺ :
 (خَيْرُ يَوْمٍ طَلَعَتْ عَلَيْهِ الشَّمْسُ يَوْمُ الْجُمُعَةِ، فِيهِ خُلِقَ آدَمُ، وَفِيهِ أُدْخِلَ الْجَنَّةَ، وَفِيهِ أُخْرِجَ مِنْهَا). رواه مسلم

**سنن الجمعة**
1- الاغتسال
2- التطيب
3- التبكير إلى المسجد
4- تحرى ساعة الإجابة
5- لبس أحسن الثياب
6- كثرة الصلاة على النبي صلى الله عليه وسلم
7- قراءة سورة الكهف
8- التسوك
"""

# متغير لتخزين الشات آي دي
chat_id = None

def send_message(context: CallbackContext, text: str):
    global chat_id
    if chat_id:
        context.bot.send_message(chat_id=chat_id, text=text)
    else:
        logger.warning("chat_id غير معرف بعد، لا يمكن إرسال الرسالة")

def start(update: Update, context: CallbackContext):
    global chat_id
    chat_id = update.effective_chat.id
    update.message.reply_text("📿 تم تفعيل إرسال الأذكار التلقائي، ويمكنك استخدام الأوامر لإرسال الأذكار يدوياً.\n\nاكتب /help لمعرفة الأوامر.")

def send_morning_command(update: Update, context: CallbackContext):
    update.message.reply_text(MORNING_AZKAR)

def send_evening_command(update: Update, context: CallbackContext):
    update.message.reply_text(EVENING_AZKAR)

def send_friday_command(update: Update, context: CallbackContext):
    update.message.reply_text(FRIDAY_AZKAR)

def help_command(update: Update, context: CallbackContext):
    help_text = """
أوامر البوت:
/start - تفعيل البوت وبدء إرسال الأذكار التلقائية
/morning - إرسال أذكار الصباح الآن
/evening - إرسال أذكار المساء الآن
/friday - إرسال أذكار الجمعة الآن
/help - عرض هذه الرسالة
"""
    update.message.reply_text(help_text)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # تعيين أوامر البوت لتظهر في قائمة الأوامر بتليجرام
    updater.bot.set_my_commands([
        BotCommand("start", "تفعيل البوت وبدء إرسال الأذكار"),
        BotCommand("morning", "أرسل أذكار الصباح الآن"),
        BotCommand("evening", "أرسل أذكار المساء الآن"),
        BotCommand("friday", "أرسل أذكار الجمعة الآن"),
        BotCommand("help", "عرض أوامر البوت"),
    ])

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("morning", send_morning_command))
    dp.add_handler(CommandHandler("evening", send_evening_command))
    dp.add_handler(CommandHandler("friday", send_friday_command))
    dp.add_handler(CommandHandler("help", help_command))

    # إعداد الجدولة مع توقيت القاهرة
    tz = pytz.timezone("Africa/Cairo")
    scheduler = BackgroundScheduler(timezone=tz)
    scheduler.add_job(send_message, 'cron', hour=4, minute=25, args=[updater.bot, MORNING_AZKAR])
    scheduler.add_job(send_message, 'cron', hour=20, minute=6, args=[updater.bot, EVENING_AZKAR])
    scheduler.add_job(send_message, 'cron', day_of_week='fri', hour=7, minute=0, args=[updater.bot, FRIDAY_AZKAR])
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
