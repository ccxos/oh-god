from telebot import TeleBot, types
import requests

bot = TeleBot("8142403647:AAHfJjncTAphNkJn-6YahCmWqpRKfTriBMg")

#X

b = types.InlineKeyboardMarkup(row_width=1)
back = types.InlineKeyboardButton(text="X", url="https://t.me/ueoot")
b.add(back)

#ID C

IDCH = -1002230950376
JOIN_LINK = "https://t.me/+21tmta-dfkJlZmUx"

#GITHUB TXT RAW

GITHUB_RAW_URL = "https://raw.githubusercontent.com/ccxos/oh-god/refs/heads/main/videos.txt"

#Load videos from GitHub once

def load_videos():
    videos = {}
    try:
        r = requests.get(GITHUB_RAW_URL)
        lines = r.text.strip().splitlines()
        for line in lines:
            if "|" in line:
                name, url = line.strip().split("|", 1)
                videos[name.strip()] = url.strip()
    except Exception as e:
        print("Error loading videos:", e)
    return videos

#Load videos once into memory

videos = load_videos()

#C (Videos List)

def generate_buttons():
    c = types.InlineKeyboardMarkup(row_width=1)
    for name in videos:
        btn = types.InlineKeyboardButton(text=name, callback_data=name)
        c.add(btn)
    return c

#sub

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(chat_id=IDCH, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

#start

@bot.message_handler(commands=["start"])
def start(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"You need to join {JOIN_LINK} first, then /start.")
        return
    bot.reply_to(message, "Hi! Here you can find your dream.", reply_markup=b)

#show

@bot.message_handler(commands=["show"])
def show(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"You need to join {JOIN_LINK} first, then /start.")
        return
    c = generate_buttons()
    bot.reply_to(message, "Choose your favorite :", reply_markup=c)

#button

@bot.callback_query_handler(func=lambda call: True)
def query(call):
    if not is_subscribed(call.from_user.id):
        bot.send_message(call.message.chat.id, f"You need to join {JOIN_LINK} first, then /start.")
        return
    name = call.data
    if name in videos:
        url = videos[name]
        caption = f"{name} | sex scene."
        bot.send_video(call.message.chat.id, url, caption=caption, reply_markup=b)

bot.polling()
