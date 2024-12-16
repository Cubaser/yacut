import os
import string


CHARS = string.ascii_letters + string.digits
MAX_RETRIES = 10
SHORT_LINK_LENGTH = 6
CUSTOM_ID_MAX_LEN = 16
CUSTOM_ID_PATTERN = r'[A-Za-z0-9]*$'
MESSAGE_URL_DONE = 'Ваша короткая ссылка готова:'
MESSAGE_URL_FAIL = 'Предложенный вариант короткой ссылки уже существует.'
API_MESSAGE_URL_FAIL = '\"url\" является обязательным полем!'
API_MESSAGE_BODY_FAIL = 'Отсутствует тело запроса'
API_MESSAGE_CUSTOM_ID_FAIL = 'Указанный id не найден'
API_MESSAGE_BAD_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
API_MESSAGE_DOUBLE_CUSTOM_ID = ('Предложенный вариант короткой '
                                'ссылки уже существует.')


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
