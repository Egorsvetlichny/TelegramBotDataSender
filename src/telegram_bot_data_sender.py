import logging
import random
from telebot import types

from bot_functions import *
from bot_typical_answers import *
from console_logger import logger
from func_tools import get_user_full_name


@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Инфо")
    button2 = types.KeyboardButton("Помощь")
    button3 = types.KeyboardButton("Выбрать вакансию")
    button4 = types.KeyboardButton("Заполнить анкету")
    keyboard.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, "Привет! Я бот, который готов помочь вам! "
                                      "Чтобы узнать о моих возможностях, "
                                      "воспользуйтесь командой /help или напишите 'помощь'", reply_markup=keyboard)

    with open(r'C:\Users\fkhor\PycharmProjects\TelegramBotDataSender\content\greeting.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)

    logger.info("Пользователь %s начал диалог", get_user_full_name(message))


@bot.message_handler(func=lambda message: any(vacancy in message.text for vacancy in vacancy_functions))
def handle_vacancys(message):
    globals()[message.text.replace('/', '')](message)


@bot.message_handler(commands=['info'])
def handle_info(message):
    response = ("Итак, я - бот для рассылки контактной информации, "
                "чтобы с вами можно было связаться доступно и быстро! \n"
                "Основная моя функция - /forward. \n"
                "Используй ее, чтобы переслать свои актуальные контактные данные для последующей обратной связи!")
    bot.send_message(message.chat.id, response)

    logger.info("Пользователь %s воспользовался справкой", get_user_full_name(message))


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, help_response)

    logger.info("Пользователь %s использовал функцию помощи", get_user_full_name(message))


@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in hi_words))
def handle_hi(message):
    reply = random.choice(hi_answers)
    bot.reply_to(message, reply)

    logger.info("Пользователь %s поздоровался с ботом", get_user_full_name(message))


@bot.message_handler(func=lambda message: any(phrase in message.text.lower() for phrase in how_are_you_phrases))
def handle_how_are_you(message):
    reply = random.choice(how_are_you_answers)
    bot.reply_to(message, reply)

    logger.info("Пользователь %s спросил у бота, как дела", get_user_full_name(message))


@bot.message_handler(func=lambda message: any(phrase in message.text.lower() for phrase in help_phrases))
def handle_help_messages(message):
    handle_help(message)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == 'Инфо':
        handle_info(message)
    elif message.text == 'Помощь':
        handle_help(message)
    elif message.text == 'Выбрать вакансию':
        vacancy_choice(message)
    elif message.text == 'Заполнить анкету' or message.text == '/forward':
        forward_message(message)
    else:
        response = random.choice(all_answers)
        bot.send_message(message.chat.id, response)

        logger.info("Пользователь %s отправил сообщение: %s", get_user_full_name(message), message.text)


if __name__ == '__main__':
    bot.polling()
    logging.shutdown()
