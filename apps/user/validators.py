import re
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(phone_number: str) -> ValidationError | str:
    """Валидатор номера телефона на соответствие формату Казахстана"""

    cleaned_phone_number = re.sub(r"[^\d+]", "", phone_number)
    if re.match(r'^\+7\d{10}$', cleaned_phone_number):
        return '+' + cleaned_phone_number[1:]
    else:
        raise ValidationError(_('Телефонный номер должен быть в формате +7 (xxx) xxx-xx-xx'))
