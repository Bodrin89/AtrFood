from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.promotion.models import LoyaltyModel
from apps.user.models import AddressModel, BaseUserModel


class ContactPersonModel(models.Model):
    class Meta:
        verbose_name = _('Контактное лицо')
        verbose_name_plural = _('Контактные лица')

    surname = models.CharField(max_length=255, verbose_name=_('фамилия'))
    first_name = models.CharField(max_length=255, verbose_name=_('имя'))
    second_name = models.CharField(max_length=255, verbose_name=_('отчество'))

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.second_name}'


class CompanyAddress(AddressModel):
    class Meta:
        verbose_name = _('Адрес Компании')
        verbose_name_plural = _('Адреса компаний')

    country = models.CharField(max_length=255, verbose_name=_('страна'))
    office_number = models.PositiveSmallIntegerField(verbose_name=_('номер офиса'))
    apartment_number = None
    floor = None

    def __str__(self):
        return self.country


class CompanyUserModel(BaseUserModel):
    class Meta:
        verbose_name = _('Юридическое лицо')
        verbose_name_plural = _('Юридические лица')

    class PaymentMethod(models.TextChoices):
        CASH = ('cash', _('Cache'))
        NON_CASH = ('non_cash', _('Non_cash'))

    company_name = models.CharField(max_length=255, verbose_name=_('название компании'))
    bin_iin = models.PositiveBigIntegerField(verbose_name=_('БИН/ИИН'))
    iik = models.CharField(max_length=255, verbose_name=_('ИИК'))
    bank = models.CharField(max_length=255, verbose_name=_('IBAN'))
    bik = models.CharField(max_length=255, verbose_name=_('БИК'))
    company_address = models.ForeignKey(CompanyAddress, on_delete=models.CASCADE, verbose_name=_('Адрес компании'))
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.NON_CASH,
                                      verbose_name=_('способ оплаты'))
    contact_person = models.ForeignKey(ContactPersonModel, on_delete=models.CASCADE, verbose_name=_('контактное лицо'))
    loyalty = models.ForeignKey(LoyaltyModel, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                verbose_name=_('Уровень системы лояльности'))
