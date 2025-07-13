import time
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "7674655190:AAEUxpXd5P-Z-SEzmo7qKnxXlyhnG9JcVqg"
CHAT_ID = "-1002470716958"

messages = [
    "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
    "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ",
    "لا حَوْلَ ولا قوَّةَ إلَّا باللهِ"
]

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="أهلاً بيك في بوت الأذكار! 🌟\n"
                                  "أنا هنا عشان أذكرك بالأذكار المفيدة والجميلة على مدار اليوم.\n"
                                  "استخدم الأوامر عشان تتحكم في البوت بسهولة.")

def activate(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="تم تفعيل الخدمة بنجاح! 🔥\n"
                                  "هتوصلك الرسائل التلقائية بإذن الله.\n"
                                  "لو عايز توقف الخدمة، ابعت /stop")

def send_messages(context):
    i = context.job.context.get("index", 0)
    context.bot.send_message(chat_id=CHAT_ID, text=messages[i])
    context.job.context["index"] = (i + 1) % len(messages)

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # أوامر المستخدم
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("activate", activate))

    # تكرار الرسائل التلقائي كل 30 دقيقة
    job_queue = updater.job_queue
    job_queue.run_repeating(send_messages, interval=1800, first=0, context={"index": 0})

    # تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
