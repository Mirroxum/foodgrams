from re import compile

from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class OneOfTwoValidator:
    ru_regex = '[^а-яёА-ЯЁ]+'
    en_regex = '[^a-zA-Z]+'
    message = (
        'Переданное значение на разных языках либо содержит что-то кроме букв.'
    )

    def __init__(self, ru_regex=None, en_regex=None, message=None):
        if ru_regex is not None:
            self.ru_regex = ru_regex
        if en_regex is not None:
            self.en_regex = en_regex
        if message is not None:
            self.message = message

        self.ru_regex = compile(self.ru_regex)
        self.en_regex = compile(self.en_regex)

    def __call__(self, value):
        if self.ru_regex.search(value) and self.en_regex.search(value):
            raise ValidationError(self.message)


@deconstructible
class MinLenValidator:
    min_len = 0
    message = 'Переданное значение слишком короткое.'

    def __init__(self, min_len=None, message=None):
        if min_len is not None:
            self.min_len = min_len
        if message is not None:
            self.message = message

    def __call__(self, value):
        if len(value) < self.min_len:
            raise ValidationError(self.message)


@deconstructible
class UsernameNotMeValidator:
    username = 'me'
    message = f'Невозможно использовать {username} как username'

    def __init__(self, username=None, message=None):
        if username is not None:
            self.username = username
        if message is not None:
            self.message = message

    def __call__(self, value):
        if value == self.username:
            raise ValidationError(self.message)
