import random

import telebot

from src.id_tokens import tg_bot_token, chat_id_superuser
from src.bot_typical_answers import hi_answers, all_answers

bot = telebot.TeleBot(tg_bot_token)


@bot.message_handler(commands=['forward'])
def forward_message(message):
    bot.forward_message(chat_id_superuser, message.chat.id, message.message_id)


@bot.message_handler(commands=['help'])
def handle_help(message):
    response = "Привет! Используй мои возможности с помощью одной из следующих команд: \n" \
               "/start - Начать диалог с ботом \n" \
               "/help - Получить помощь \n" \
               "/forward - Отправить контактную информацию администратору\n" \
               "/info - Получить информацию о боте"
    bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: 'привет' in message.text.lower())
def handle_how_are_you(message):
    reply = random.choice(hi_answers)
    bot.reply_to(message, reply)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    response = random.choice(all_answers)
    bot.send_message(message.chat.id, response)


bot.polling()
