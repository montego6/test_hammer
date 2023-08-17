import string
import random


def generate_login_code():
    return ''.join(random.choices(string.digits, k=4))


def generate_invite_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))