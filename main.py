import time
import telegram

BOT_TOKEN = "7674655190:AAEUxpXd5P-Z-SEzmo7qKnxXlyhnG9JcVqg"
CHAT_ID = "1438736069"

messages = [
    "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
    "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ",
    "لا حَوْلَ ولا قوَّةَ إلَّا باللهِ"
]

bot = telegram.Bot(token=BOT_TOKEN)

def send_messages():
    i = 0
    while True:
        bot.send_message(chat_id=CHAT_ID, text=messages[i])
        print(f"Sent: {messages[i]}")
        i = (i + 1) % len(messages)
        time.sleep(1800)  # 30 دقيقة = 1800 ثانية

if __name__ == "__main__":
    send_messages()
