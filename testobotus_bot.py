import telebot
import sqlite3
from telebot import types
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CH_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(TOKEN)
if not TOKEN:
    raise ValueError("Токен не найден в переменных окружения!")

# bot = telebot.TeleBot(token='8385780029:AAF3FTM_ZMmTZw90eSVC_py3SqpXG4d4Gbo')

name = ""
tel = ""
other_ans = ""

def bot_message(chatId, name, tel, aim):
    bot.send_message(chat_id=chatId, text=f"Имя: {name}, тел: {tel}, цель: {aim}")

def bye_message(var):
    bot.send_message(var.message.chat.id, "Я успешно сохранил ваши данные, ждите звонка по вашему запросу")

def ins_bd(name, tel, aim):
    conn = sqlite3.connect("TeleBot_SQL.db")
    cur = conn.cursor()
    dt = datetime.now()
    str_dt = dt.strftime("%Y-%m-%d %H:%M")

    cur.execute("INSERT INTO users (name, tel, aim, datetime) VALUES (?, ?, ?, ?)", (name, tel, aim, str_dt))
    conn.commit()

    cur.close()
    conn.close()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}")
    bot.send_message(message.chat.id, "Я помогу вам с решением пикантных вопросов в оформлении документов.")
    bot.send_message(message.chat.id, "Чтобы я мог помочь вам персонально, пожалуйста, пройдите короткую регистрацию.")

    conn = sqlite3.connect("TeleBot_SQL.db")
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), tel varchar(50), aim varchar(100), datetime varchar(50))")
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Введите своё имя")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите номер телефона")
    bot.register_next_step_handler(message, user_tel)

def user_tel(message):
    global tel
    tel = message.text.strip()

    markup = types.InlineKeyboardMarkup()
    btn02 = types.InlineKeyboardButton("Книжка", callback_data="Книжка")
    btn03 = types.InlineKeyboardButton("Билет", callback_data="Билет")
    btn04 = types.InlineKeyboardButton("Услуга", callback_data="Услуга")
    btn05 = types.InlineKeyboardButton("Другое", callback_data="Другое")
    markup.row(btn02, btn03)
    markup.row(btn04, btn05)
    bot.send_message(message.chat.id, "Выберите интересующий документ или напишите,что нужно", reply_markup=markup)

# создаём функции для обработки кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "Книжка":
        ins_bd(name, tel, callback.data)
        bye_message(callback)
        bot_message(CH_ID, name,tel, callback.data)
    elif callback.data == "Билет":
        ins_bd(name, tel, callback.data)
        bye_message(callback)
        bot_message(CH_ID, name, tel, callback.data)
    elif callback.data == "Услуга":
        ins_bd(name, tel, callback.data)
        bye_message(callback)
        bot_message(CH_ID, name, tel, callback.data)
    elif callback.data == "Другое":
        bot.send_message(callback.message.chat.id, "Введите, что вам нужно")
        bot_message(CH_ID, name, tel, callback.data)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global other_ans
    other_ans = message.text.strip()
    ins_bd(name, tel, other_ans)
    bot.send_message(message.chat.id, "Я успешно сохранил ваши данные, ждите звонка по вашему запросу")
    bot_message(8147334737, name, tel, other_ans)

bot.infinity_polling()
