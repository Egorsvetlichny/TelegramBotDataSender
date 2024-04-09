import logging
import random
from telebot import types

import telebot
from telebot.types import ReplyKeyboardMarkup

from id_tokens import tg_bot_token, admin_chat_id
from bot_typical_answers import *
from console_logger import logger
from func_tools import get_user_full_name

bot = telebot.TeleBot(tg_bot_token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Инфо")
    button2 = types.KeyboardButton("Помощь")
    button3 = types.KeyboardButton("Выбрать вакансию")
    keyboard.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Привет! Я бот, который готов помочь вам! "
                                      "Чтобы узнать о моих возможностях, "
                                      "воспользуйтесь командой /help или напишите 'помощь'", reply_markup=keyboard)

    logger.info("Пользователь %s начал диалог.", get_user_full_name(message))


@bot.message_handler(commands=['vacancy'])
def vacancy_choice(message):
    response = "/kassir | Кассир - ... \n" \
               "/start - Начать диалог с ботом \n" \
               "/help - Получить помощь \n" \
               "/forward - Отправить контактную информацию администратору\n" \
               "/info - Получить информацию о боте"

    bot.send_message(message.chat.id, response)

    logger.info('Пользователь %s нажал на кнопку "Выбрать вакансию"', get_user_full_name(message))


# Блок функции forward
@bot.message_handler(commands=['forward'])
def forward_message(message):
    bot.send_message(message.chat.id, "Укажите свою Фамилию и Имя")
    bot.register_next_step_handler(message, remember_user_fio)

    logger.info("Пользователь %s использовал функцию forward.", get_user_full_name(message))


def remember_user_fio(message):
    data_arr = [' '.join(message.text.split()[1:]), message.text]
    bot.send_message(message.chat.id, "Укажите дату рождения в формате: дд.мм.гггг")
    bot.register_next_step_handler(message, remember_user_birthdate, data_arr)

    logger.info("Пользователь %s указал своё ФИО", get_user_full_name(message))


def remember_user_birthdate(message, data_arr):
    data_arr.append(message.text)
    bot.send_message(message.chat.id, "Укажите контактный номер телефона")
    bot.register_next_step_handler(message, remember_user_phone_number, data_arr)

    logger.info("Пользователь %s указал свою дату рождения", get_user_full_name(message))


def remember_user_phone_number(message, data_arr):
    data_arr.append(message.text)
    bot.send_message(message.chat.id, "Укажите город фактического проживания")
    bot.register_next_step_handler(message, send_all_data_to_admin, data_arr)

    logger.info("Пользователь %s указал свой номер телефона", get_user_full_name(message))


def send_all_data_to_admin(message, data_arr):
    bot.send_message(admin_chat_id, f"{data_arr[1]} \n{data_arr[2]} \n{data_arr[3]} \n{message.text}")
    text = f"Спасибо, что указали свои контактные данные, {data_arr[0]}! В ближайшее время с вами обязательно свяжутся!"
    bot.send_message(message.chat.id, text)

    logger.info("Пользователь %s указал свой город", get_user_full_name(message))


@bot.message_handler(commands=['info'])
def handle_info(message):
    response = ("Итак, я - бот для рассылки контактной информации, "
                "чтобы с вами можно было связаться доступно и быстро! \n"
                "Основная моя функция - /forward. \n"
                "Используй ее, чтобы переслать свои актуальные контактные данные для последующей обратной связи!")
    bot.send_message(message.chat.id, response)

    logger.info("Пользователь %s воспользовался справкой.", get_user_full_name(message))


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, help_response)

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


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == 'Инфо':
        handle_info(message)
    elif message.text == 'Помощь':
        handle_help(message)
    elif message.text == 'Выбрать вакансию':
        vacancy_choice(message)
    else:
        response = random.choice(all_answers)
        bot.send_message(message.chat.id, response)

        logger.info("Пользователь %s отправил сообщение: %s", get_user_full_name(message), message.text)


if __name__ == '__main__':
    bot.polling()
    logging.shutdown()
