import telebot
import requests
from datetime import datetime
from telebot import types
from dotenv import load_dotenv
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
SERVER_URL = "http://127.0.0.1:8080"
ADMIN_ID = 6154565499


@bot.message_handler(commands=['start'])  # стартовая команда
def start(message):
    if message.chat.id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton('➕ добавить копмлектацию')
        markup.add(btn1)

        bot.reply_to(message, "🛠 Админ-панель:", reply_markup=markup)
        return

user_data = {}

@bot.message_handler(func=lambda message: message.text == '➕ добавить копмлектацию')
def start_slot(message):
    chat_id = message.chat.id
    if chat_id != ADMIN_ID:
        bot.reply_to(message, "вы не являетесь администратором")
        return
    user_data[message.chat.id] = {}
    bot.reply_to(message, "📝 Введите название:")
    bot.register_next_step_handler(message, get_master_name_slot)

def get_master_name_slot(message):
    chat_id = message.chat.id
    user_data[chat_id]['start_time'] = message.text if message.text != '-' else 'Не указан'
    bot.reply_to(message, "введите категори:")
    bot.register_next_step_handler(message, get_review_text_slot)

def get_review_text_slot(message):
    chat_id = message.chat.id
    user_data[chat_id]['end_time'] = message.text
    bot.reply_to(message, "введите номер:")
    bot.register_next_step_handler(message, get_rating_slot)

def get_rating_slot(message):
    chat_id = message.chat.id
    if message.text == "назад":
        bot.reply_to(message, "вы вышли из добавления комплектации") 
        return

    user_data[chat_id]['status'] = message.text

    # Теперь у нас есть все данные
    data = user_data[chat_id]


    response = requests.get(f"https://server-for-mir-j-production.up.railway.app/add_warehouse?name={user_data[chat_id]['start_time']}&quantity=10&category={user_data[chat_id]['end_time']}&number={user_data[chat_id]['status']}")
    if response.status_code == 200:
        bot.reply_to(message,
                     f"время добавлено!\n🕟название - {data['start_time']}\n🕟категория - {data['end_time']}\nномер - {data['status']}\n")
    else:
        bot.reply_to(message, "ошибка сервера")
        return

    del user_data[chat_id]  # Очищаем данные пользователя

if __name__ == '__main__':
    bot.infinity_polling()
