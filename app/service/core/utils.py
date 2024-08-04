import string
import secrets

from datetime import datetime
from babel.support import Translations

from passlib.context import CryptContext
from core.config import Config


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def gettext(message: str) -> str:
    return message


def unixify_timestamp(date: datetime) -> int:
    return int(datetime.timestamp(date))


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def generate_random_integers(length=10):
    return ''.join(secrets.choice(string.digits) for letter in range(length))


def generate_random_alnum_string(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for letter in range(length))


class TranslationClass:
    def __init__(self, language='en'):
        self.language = language
        self.translations = self.load_translations()

    def load_translations(self):
        translations = Translations.load(Config.LOCALES_PATH, locales=[self.language])
        return translations

    def gettext(self, message):
        return self.translations.gettext(message)
