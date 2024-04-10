import re


def validate_city(city_name):
    pattern = re.compile("[а-яёА-ЯЁ\s\-]+")

    if pattern.fullmatch(city_name):
        return True
    else:
        return False
