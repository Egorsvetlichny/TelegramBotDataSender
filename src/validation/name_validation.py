def validate_name(name):
    name_parts = name.split()

    if len(name_parts) != 2:
        return False

    if not name_parts[0].isalpha() or not name_parts[1].isalpha():
        return False

    return True
