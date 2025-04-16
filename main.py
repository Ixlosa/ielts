import os, json
import telebot
from telebot import types

TOKEN = os.environ["7708038290:AAGT7-Lw4BU8d-6lyPzoBJA5NuRL1SXMrjA"]
bot = telebot.TeleBot(TOKEN)
PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

progress = load_progress()

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('Reading','Listening')
    kb.row('My Progress')
    bot.send_message(m.chat.id, "Welcome to IELTS Bot!", reply_markup=kb)

@bot.message_handler(func=lambda m: True)
def msg(m):
    uid = str(m.from_user.id)
    if uid not in progress:
        progress[uid] = {"Reading":0,"Listening":0}
    if m.text == 'Reading':
        progress[uid]["Reading"] += 1
        bot.send_message(m.chat.id, f"Reading +1 → {progress[uid]['Reading']}")
    elif m.text == 'Listening':
        progress[uid]["Listening"] += 1
        bot.send_message(m.chat.id, f"Listening +1 → {progress[uid]['Listening']}")
    elif m.text == 'My Progress':
        r,l = progress[uid]["Reading"], progress[uid]["Listening"]
        bot.send_message(m.chat.id, f"📊 Reading: {r}\nListening: {l}")
    else:
        bot.send_message(m.chat.id, "Выбери кнопку.")
    save_progress(progress)

if __name__ == '__main__':
    bot.infinity_polling()
