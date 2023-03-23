import datetime
import re

from rest_framework.validators import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            '"me" в качестве логина использовать нельзя!'
        )
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'Введены некоректные символы!'
        )
    return value


def validate_year(value):
    if value > datetime.date.today().year:
        raise ValidationError(
            'Машина времени ещё не изобретена, поменяй год!'
        )
    return value
