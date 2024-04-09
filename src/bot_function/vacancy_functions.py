from bot_typical_answers import *
from console_logger import logger
from func_tools import get_user_full_name
from telegram_bot_data_sender import bot

vacancys_function = [
    '/vacancy',
    '/cashier',
    '/sales_consultant',
    '/barista',
    '/sales_worker',
    '/order_picker',
    '/other_vacancies',
]


@bot.message_handler(commands=['vacancy'])
def vacancy_choice(message):
    bot.send_message(message.chat.id, vacancy_response)

    logger.info('Пользователь %s нажал на кнопку "Выбрать вакансию"', get_user_full_name(message))


@bot.message_handler(commands=['cashier'])
def cashier(message):
    text = 'Уникальное сообщение'
    bot.send_message(message.chat.id, text)

    logger.info('Пользователь %s выбрал вакансию кассира', get_user_full_name(message))


@bot.message_handler(commands=['sales_consultant'])
def sales_consultant(message):
    text = 'Уникальное сообщение'
    bot.send_message(message.chat.id, text)

    logger.info('Пользователь %s выбрал вакансию продавца-консультанта', get_user_full_name(message))


@bot.message_handler(commands=['barista'])
def barista(message):
    text = 'Уникальное сообщение'
    bot.send_message(message.chat.id, text)

    logger.info('Пользователь %s выбрал вакансию бариста', get_user_full_name(message))


@bot.message_handler(commands=['sales_worker'])
def sales_worker(message):
    text = 'Уникальное сообщение'
    bot.send_message(message.chat.id, text)

    logger.info('Пользователь %s выбрал вакансию работника торгового зала', get_user_full_name(message))


@bot.message_handler(commands=['order_picker'])
def order_picker(message):
    text = 'Уникальное сообщение'
    bot.send_message(message.chat.id, text)

    logger.info('Пользователь %s выбрал вакансию сборщика заказов', get_user_full_name(message))


@bot.message_handler(commands=['other_vacancies'])
def other_vacancies(message):
    text = 'Уникальное сообщение'
    bot.send_message(message.chat.id, text)

    logger.info('Пользователь %s выбрал другие вакансии', get_user_full_name(message))
