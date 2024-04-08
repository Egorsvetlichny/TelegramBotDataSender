def get_user_full_name(message):
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    if user_last_name:
        full_name = f"{user_last_name} {user_first_name}"
    else:
        full_name = user_first_name

    return full_name
