import random
from string import digits, ascii_letters

from .models import URLMap

SYMBOLS_CHOICE = list(digits + ascii_letters)


def custom_link_view():
    link = random.choices(SYMBOLS_CHOICE, k=6)
    return ''.join(link)


def validate_custom_link(link):
    if len(link) > 16:
        return False
    for elem in link:
        if elem not in SYMBOLS_CHOICE:
            return False
    return True


def check_unique_short_id(short_id):
    if URLMap.query.filter_by(short=short_id).first():
        return short_id
    return None