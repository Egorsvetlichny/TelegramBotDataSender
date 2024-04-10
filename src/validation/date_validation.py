import datetime


def validate_date(date_string):
    try:
        day, month, year = map(int, date_string.split('.'))

        if day < 1 or day > 31:
            return False
        if month < 1 or month > 12:
            return False
        if year < datetime.date.today().year - 100 or year > 2006:
            return False

        return True

    except ValueError:
        return False
