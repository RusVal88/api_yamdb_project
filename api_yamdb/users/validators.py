from rest_framework.validators import ValidationError


def validate_me(value):
    if value == 'me':
        raise ValidationError(
            '"me" в качестве логина использовать нельзя!')
