import random


user_names = ["Kingslayer"]


def get_user_name():
    return random.choice(user_names)


def add_user_name(new_name: str):
    user_names.append(new_name)
