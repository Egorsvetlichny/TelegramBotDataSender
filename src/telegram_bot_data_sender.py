import telebot

from src.id_tokens import tg_bot_token, chat_id_superuser


bot = telebot.TeleBot(tg_bot_token)

@bot.message_handler(commands=['forward'])
def forward_message(message):
    bot.forward_message(chat_id_superuser, message.chat.id, message.message_id)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.reply_to(message, "Для пересылки сообщения используйте команду /forward")

bot.polling()