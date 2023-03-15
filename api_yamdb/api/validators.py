import re
from rest_framework.validators import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            '"me" в качестве логина использовать нельзя!'
        )
    if not re.match(r'[\w.@+-]+\Z', value):
        raise ValidationError(
            'Введены некоректные символы!'
        )
