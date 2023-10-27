
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def bin_iin_validator(bin_iin):
    if len(str(bin_iin)) != 12:
        raise ValidationError(_('Поле bin_iin должно содержать 12 цифр'))


def bik_validator(bik):
    if len(str(bik)) != 9:
        raise ValidationError(_('Поле bik должно содержать 9 цифр'))


def iban_validator(iban):
    iban_ = iban.replace(' ', '')
    list_iban = ' '.join(iban_).split()
    if not list_iban[0:2] == ['K', 'Z']:
        raise ValidationError(_('IBAN должен начинаться с "KZ"'))
    if len(iban_) != 20:
        raise ValidationError(_('IBAN должен состоять из 20 символов'))
    return True
