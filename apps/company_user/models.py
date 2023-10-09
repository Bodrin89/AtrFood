from django.db import models

from apps.user.models import AddressModel, BaseUserModel
from django.utils.translation import gettext_lazy as _


class ContactPersonModel(models.Model):
    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'

    surname = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)


class CompanyAddress(AddressModel):
    class Meta:
        verbose_name = 'Адрес Компании'
        verbose_name_plural = 'Адреса компаний'

    pass


class CompanyUserModel(BaseUserModel):
    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    class PaymentMethod(models.TextChoices):
        CASH = ('cash', _('Cache'))
        NON_CASH = ('non_cash', _('Non_cash'))

    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    bin_iin = models.PositiveBigIntegerField()
    iik = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    bik = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.NON_CASH)
    contact_person = models.ForeignKey(ContactPersonModel, on_delete=models.CASCADE)
