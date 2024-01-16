import os


SHORT_LINK_MAX_LENGHT = 16
DEFAULT_SHORT_LINK_LENGHT = 6
REGEX_FORM_VALIDATION = '[A-Za-z0-9]*$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')