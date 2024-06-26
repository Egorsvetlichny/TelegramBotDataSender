from bot import bot
from console_logger import logger
from func_tools import get_user_full_name
from id_tokens import admin_chat_id
from validation import *


@bot.message_handler(commands=['forward'])
def forward_message(message):
    bot.send_message(message.chat.id, "Укажите свою Фамилию и Имя")
    bot.register_next_step_handler(message, remember_user_fio)

    logger.info("Пользователь %s использовал функцию forward", get_user_full_name(message))


def remember_user_fio(message):
    if not validate_name(message.text):
        bot.send_message(message.chat.id, "Неверный формат имени. "
                                          "Пожалуйста, отправьте только фамилию и имя")
        bot.register_next_step_handler(message, remember_user_fio)

        logger.info("Пользователь %s неверно указал фамилию или имя", get_user_full_name(message))
    else:
        data_arr = [' '.join(message.text.split()[1:]), message.text]
        bot.send_message(message.chat.id, "Укажите дату рождения в формате: дд.мм.гггг")
        bot.register_next_step_handler(message, remember_user_birthdate, data_arr)

        logger.info("Пользователь %s указал фамилию и имя", get_user_full_name(message))


def remember_user_birthdate(message, data_arr):
    if not validate_birthdate(message.text):
        bot.send_message(message.chat.id, "Неверный формат даты. "
                                          "Пожалуйста, отправьте дату в формате: дд.мм.гггг.")
        bot.register_next_step_handler(message, remember_user_birthdate, data_arr)

        logger.info("Пользователь %s неверно указал дату рождения", get_user_full_name(message))
    else:
        data_arr.append(message.text)
        bot.send_message(message.chat.id, "Укажите контактный номер телефона")
        bot.register_next_step_handler(message, remember_user_phone_number, data_arr)

        logger.info("Пользователь %s указал дату своего рождения", get_user_full_name(message))


def remember_user_phone_number(message, data_arr):
    phone_number = validate_phone_number(message.text)

    if not phone_number:
        bot.send_message(message.chat.id, "Неверный формат номера телефона. "
                                          "Пожалуйста, отправьте номер в формате +7XXXXXXXXXX или 8XXXXXXXXXX.")
        bot.register_next_step_handler(message, remember_user_phone_number, data_arr)

        logger.info("Пользователь %s неверно указал номер телефона", get_user_full_name(message))
    else:
        data_arr.append(phone_number[1:])
        bot.send_message(message.chat.id, "Укажите город фактического проживания")
        bot.register_next_step_handler(message, send_all_data_to_admin, data_arr)

        logger.info("Пользователь %s указал свой номер телефона", get_user_full_name(message))


def send_all_data_to_admin(message, data_arr):
    if not validate_city(message.text):
        bot.send_message(message.chat.id, "Неверный формат названия города. "
                                          "Пожалуйста, отправьте название своего города без лишних символов")
        bot.register_next_step_handler(message, send_all_data_to_admin, data_arr)

        logger.info("Пользователь %s неверно указал название города", get_user_full_name(message))
    else:
        bot.send_message(admin_chat_id, f"{data_arr[1]} \n{data_arr[2]} \n{data_arr[3]} \n{message.text}")
        text = (f"Спасибо, что указали свои контактные данные, {data_arr[0]}! "
                f"В ближайшее время с вами обязательно свяжутся!")
        bot.send_message(message.chat.id, text)

        logger.info("Пользователь %s указал свой город", get_user_full_name(message))
