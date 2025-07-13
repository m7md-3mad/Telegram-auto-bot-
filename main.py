from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "7674655190:AAHGQbac6F9ecwtp7fP0DK5B3_38cs0Jv1M"

def start(update, context):
    update.message.reply_text("أهلاً! البوت شغال دلوقتي.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
