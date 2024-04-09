import re


def validate_phone_number(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)

    if len(phone_number) != 11:
        return False

    if not phone_number.startswith('7') and not phone_number.startswith('8'):
        return False

    if phone_number[1] != '9':
        return False

    if not phone_number[1:].isdigit():
        return False

    return phone_number
