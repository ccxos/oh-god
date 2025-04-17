from telebot import TeleBot, types
import requests

bot = TeleBot("8142403647:AAHfJjncTAphNkJn-6YahCmWqpRKfTriBMg")

#ID CID

CH = -1002230950376
JOIN_LINK = "https://t.me/+21tmta-dfkJlZmUx"

#GITHUB TXT RAW

VIDEOS_URL = "https://raw.githubusercontent.com/ccxos/oh-god/refs/heads/main/videos.txt"
PORN_URL = "https://raw.githubusercontent.com/ccxos/oh-god/refs/heads/main/p0rn.txt"

#X

b = types.InlineKeyboardMarkup(row_width=1)
back = types.InlineKeyboardButton(text="X", url="https://t.me/ueoot", protect_content=True)
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

#Load p0rn text buttons with watch/download

def load_text_buttons_with_links(url):
    buttons = {}
    try:
        r = requests.get(url)
        lines = r.text.strip().splitlines()
        for line in lines:
            parts = line.strip().split("|")
            if len(parts) == 3:
                name, watch_url, download_url = map(str.strip, parts)
                buttons[name] = {"watch": watch_url, "download": download_url}
    except Exception as e:
        print("Error loading p0rn buttons:", e)
    return buttons

#C (Videos List)

def generate_buttons(videos):
    c = types.InlineKeyboardMarkup(row_width=3)
    for name in videos:
        btn = types.InlineKeyboardButton(text=name, callback_data=name, protect_content=True)
        c.add(btn)
    return c

#C (Text Buttons)

def generate_text_buttons(buttons):
    c = types.InlineKeyboardMarkup(row_width=2)
    for name in buttons:
        btn = types.InlineKeyboardButton(text=name, callback_data=f"p0rn_{name}", protect_content=True)
        c.add(btn)
    return c

#sub

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(chat_id=CH, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

#start

@bot.message_handler(commands=["start"])
def start(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"You need to join {JOIN_LINK} first, then /start.", protect_content=True)
        return
    bot.reply_to(message, "Hi! Here you can find your dream.", reply_markup=b, protect_content=True)

#show

@bot.message_handler(commands=["show"])
def show(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"You need to join {JOIN_LINK} first, then /start.", protect_content=True)
        return
    videos = load_videos(VIDEOS_URL)
    c = generate_buttons(videos)
    bot.send_message(message.chat.id, "Choose your favorite :", reply_markup=c, protect_content=True)

#p0rn

@bot.message_handler(commands=["p0rn"])
def p0rn(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"You need to join {JOIN_LINK} first, then /start.", protect_content=True)
        return
    buttons = load_text_buttons_with_links(PORN_URL)
    c = generate_text_buttons(buttons)
    bot.send_message(message.chat.id, "Choose your favorite :", reply_markup=c, protect_content=True)

#button

@bot.callback_query_handler(func=lambda call: True)
def query(call):
    if not is_subscribed(call.from_user.id):
        bot.send_message(call.message.chat.id, f"You need to join {JOIN_LINK} first, then /start.")
        return
    name = call.data
    if name.startswith("p0rn_"):
        key = name.replace("p0rn_", "")
        buttons = load_text_buttons_with_links(PORN_URL)
        if key in buttons:
            watch_url = buttons[key]["watch"]
            download_url = buttons[key]["download"]
            kb = types.InlineKeyboardMarkup(row_width=2)
            kb.add(
                types.InlineKeyboardButton("Watching", url=watch_url, protect_content=True),
                types.InlineKeyboardButton("Download", url=download_url, protect_content=True)
            )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{key} :", reply_markup=kb)
        return
    all_vids = {**load_videos(VIDEOS_URL)}
    if name in all_vids:
        url = all_vids[name]
        caption = f"{name} | scene"
        bot.send_video(call.message.chat.id, url, caption=caption, reply_markup=b, protect_content=True)

bot.polling()
