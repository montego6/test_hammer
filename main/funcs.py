import string
import random


def generate_login_code():
    return ''.join(random.choices(string.digits, k=4))