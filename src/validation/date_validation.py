from datetime import datetime, timedelta, date


def validate_date(date_string):
    try:
        day, month, year = map(int, date_string.split('.'))

        if day < 1 or day > 31:
            return False
        if month < 1 or month > 12:
            return False
        if year < date.today().year - 100 or year > 2006:
            return False

        return True

    except ValueError:
        return False


def validate_birthdate(birthdate_str):
    try:
        birthdate = datetime.strptime(birthdate_str, '%d.%m.%Y')

        eighteen_years_ago = datetime.now() - timedelta(days=365 * 18)
        if birthdate > eighteen_years_ago:
            return False

        hundred_years_ago = datetime.now() - timedelta(days=365 * 100)
        if birthdate < hundred_years_ago:
            return False

        return True

    except ValueError:
        return False
