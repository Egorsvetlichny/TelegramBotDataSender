import logging
import random

import telebot

from id_tokens import tg_bot_token, admin_chat_id
from bot_typical_answers import *
from console_logger import logger
from func_tools import get_user_full_name

bot = telebot.TeleBot(tg_bot_token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который готов помочь вам! "
                                      "Чтобы узнать о моих возможностях, "
                                      "воспользуйтесь командой /help или напишите 'помощь'")

    logger.info("Пользователь %s начал диалог.", get_user_full_name(message))


@bot.message_handler(commands=['forward'])
def forward_message(message):
    bot.send_message(message.chat.id, "Пожалуйста, напишите своё ФИО.")
    bot.register_next_step_handler(message, send_fio_to_admin)

    logger.info("Пользователь %s использовал функцию forward.", get_user_full_name(message))


def send_fio_to_admin(message):
    io = ' '.join(message.text.split()[1:])
    bot.forward_message(admin_chat_id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Укажите свою дату рождения через точку.")
    bot.register_next_step_handler(message, send_birthdate_to_admin, io)

    logger.info("Пользователь %s указал своё ФИО", get_user_full_name(message))


def send_birthdate_to_admin(message, io):
    bot.forward_message(admin_chat_id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Последним шагом, укажите серию и номер вашего паспорта.")
    bot.register_next_step_handler(message, send_passport_data_to_admin, io)

    logger.info("Пользователь %s указал свою дату рождения", get_user_full_name(message))


def send_passport_data_to_admin(message, io):
    bot.forward_message(admin_chat_id, message.chat.id, message.message_id)
    text = f"Спасибо, что указали свои контактные данные, {io}! В ближайшее время с вами обязательно свяжутся!"
    bot.send_message(message.chat.id, text)

    logger.info("Пользователь %s указал свои паспортные данные", get_user_full_name(message))


@bot.message_handler(commands=['info'])
def handle_info(message):
    response = ("Итак, я - бот для рассылки контактной информации, "
                "чтобы с вами можно было связаться доступно и быстро! \n"
                "Основная моя функция = /forward. \n"
                "Используй ее, чтобы переслать свои актуальные контактные данные для последующей обратной связи!")
    bot.send_message(message.chat.id, response)

    logger.info("Пользователь %s воспользовался справкой.", get_user_full_name(message))


@bot.message_handler(commands=['help'])
def handle_help(message):
    response = "Привет! Используй мои возможности с помощью одной из следующих команд: \n" \
               "/start - Начать диалог с ботом \n" \
               "/help - Получить помощь \n" \
               "/forward - Отправить контактную информацию администратору\n" \
               "/info - Получить информацию о боте"
    bot.send_message(message.chat.id, response)

    logger.info("Пользователь %s использовал функцию помощи.", get_user_full_name(message))


@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in hi_words))
def handle_hi(message):
    reply = random.choice(hi_answers)
    bot.reply_to(message, reply)

    logger.info("Пользователь %s поздоровался с ботом.", get_user_full_name(message))


@bot.message_handler(func=lambda message: any(phrase in message.text.lower() for phrase in how_are_you_phrases))
def handle_how_are_you(message):
    reply = random.choice(how_are_you_answers)
    bot.reply_to(message, reply)

    logger.info("Пользователь %s спросил у бота, как дела.", get_user_full_name(message))


@bot.message_handler(func=lambda message: any(phrase in message.text.lower() for phrase in help_phrases))
def handle_help_messages(message):
    handle_help(message)

    logger.info("Пользователь %s попросил помощи по функционалу бота", get_user_full_name(message))


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    response = random.choice(all_answers)
    bot.send_message(message.chat.id, response)

    logger.info("Пользователь %s отправил сообщение: %s", get_user_full_name(message), message.text)


if __name__ == '__main__':
    bot.polling()
    logging.shutdown()
