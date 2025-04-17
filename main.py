from telebot import TeleBot, types
import requests

bot = TeleBot("8142403647:AAHfJjncTAphNkJn-6YahCmWqpRKfTriBMg")

#ID C

IDCH = -1002230950376
JOIN_LINK = "https://t.me/+21tmta-dfkJlZmUx"

#GITHUB TXT RAW

VIDEOS_URL = "https://raw.githubusercontent.com/ccxos/oh-god/refs/heads/main/videos.txt"
PORN_URL = "https://raw.githubusercontent.com/ccxos/oh-god/refs/heads/main/p0rn.txt"

#X

b = types.InlineKeyboardMarkup(row_width=1)
back = types.InlineKeyboardButton(text="X", url="https://t.me/ueoot",protect_content=True)
b.add(back)

#Load videos from GitHub once

def load_videos(url):
    videos = {}
    try:
        r = requests.get(url)
        lines = r.text.strip().splitlines()
        for line in lines:
            if "|" in line:
                name, link = line.strip().split("|", 1)
                videos[name.strip()] = link.strip()
    except Exception as e:
        print("Error loading:", e)
    return videos

#Load p0rn text buttons

def load_text_buttons(url):
    buttons = {}
    try:
        r = requests.get(url)
        lines = r.text.strip().splitlines()
        for line in lines:
            if "|" in line:
                name, msg = line.strip().split("|", 1)
                buttons[name.strip()] = msg.strip()
    except Exception as e:
        print("Error loading p0rn text buttons:", e)
    return buttons

#C (Videos List)

def generate_buttons(videos):
    c = types.InlineKeyboardMarkup(row_width=3)
    for name in videos:
        btn = types.InlineKeyboardButton(text=name, callback_data=name,protect_content=True)
        c.add(btn)
    return c

#C (Text Buttons)

def generate_text_buttons(buttons):
    c = types.InlineKeyboardMarkup(row_width=2)
    for name in buttons:
        btn = types.InlineKeyboardButton(text=name, callback_data=f"p0rn_{name}",protect_content=True)
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
        bot.send_message(message.chat.id, f"You need to join {JOIN_LINK} first, then /start.",protect_content=True)
        return
    bot.reply_to(message, "Hi! Here you can find your dream.", reply_markup=b,protect_content=True)

#show

@bot.message_handler(commands=["show"])
def show(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"You need to join {JOIN_LINK} first, then /start.",protect_content=True)
        return
    videos = load_videos(VIDEOS_URL)
    c = generate_buttons(videos)
    bot.send_message(message.chat.id, "Choose your favorite :", reply_markup=c,protect_content=True)

#p0rn

@bot.message_handler(commands=["p0rn"])
def p0rn(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"You need to join {JOIN_LINK} first, then /start.",protect_content=True)
        return
    buttons = load_text_buttons(PORN_URL)
    c = generate_text_buttons(buttons)
    bot.send_message(message.chat.id, "Choose your favorite :", reply_markup=c,protect_content=True)

#button

@bot.callback_query_handler(func=lambda call: True)
def query(call):
    if not is_subscribed(call.from_user.id):
        bot.send_message(call.message.chat.id, f"You need to join {JOIN_LINK} first, then /start.")
        return
    name = call.data
    if name.startswith("p0rn_"):
        key = name.replace("p0rn_", "")
        buttons = load_text_buttons(PORN_URL)
        if key in buttons:
            bot.send_message(call.message.chat.id, buttons[key], reply_markup=b,protect_content=True)
        return
    all_vids = {**load_videos(VIDEOS_URL)}
    if name in all_vids:
        url = all_vids[name]
        caption = f"{name} | scene"
        bot.send_video(call.message.chat.id, url, caption=caption, reply_markup=b)

bot.polling()
