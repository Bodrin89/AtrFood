
from rest_framework.exceptions import ValidationError


def validate_phone_number(phone_number: str) -> ValidationError | str:
    """Валидатор номера телефона на соответствие формату Казахстана"""

    phone_number.split()
    list_number = ' '.join(phone_number).split()
    if list_number[0:2] != ['+', '7']:
        raise ValidationError('The country code must start with "+7"')
    if not len(list_number[2::]) == 10:
        raise ValidationError('The number must be in the format +7 (xxx) xxx-xx-xx, or 8 (xxx) xxx-xx-xx')
    return phone_number
