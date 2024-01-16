import random
from string import digits, ascii_letters

from .models import URLMap
from settings import DEFAULT_SHORT_LINK_LENGHT, SHORT_LINK_MAX_LENGHT


SYMBOLS_CHOICE = list(digits + ascii_letters)


def get_unique_short_id():
    link = random.choices(SYMBOLS_CHOICE, k=DEFAULT_SHORT_LINK_LENGHT)
    return ''.join(link)


def check_url_symbols(link):
    if len(link) > SHORT_LINK_MAX_LENGHT:
        return False
    for elem in link:
        if elem not in SYMBOLS_CHOICE:
            return False
    return True


def check_unique_short_id(custom_id):
    if URLMap.query.filter_by(short=custom_id).first():
        return custom_id
    return None