from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.promotion.models import LoyaltyModel
from apps.user.models import BaseUserModel
from apps.clients.models import AddressModel


class ContactPersonModel(models.Model):
    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'

    surname = models.CharField(max_length=255, verbose_name='фамилия')
    first_name = models.CharField(max_length=255, verbose_name='имя')
    second_name = models.CharField(max_length=255, verbose_name='отчество')

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.second_name}'


class CompanyAddress(models.Model):
    class Meta:
        verbose_name = 'Адрес Компании'
        verbose_name_plural = 'Адреса компаний'

    district = models.CharField(max_length=255, blank=True, null=True, verbose_name='район')
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name='улица')
    house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='номер дома')
    country = models.CharField(max_length=255, verbose_name='страна')
    office_number = models.PositiveSmallIntegerField(verbose_name='номер офиса')
    user = models.OneToOneField(
        BaseUserModel,
        on_delete=models.CASCADE,
        related_name='company_addresses',
        null=True,
        verbose_name='пользователь'
    )

    def __str__(self):
        return self.country


class CompanyUserModel(BaseUserModel):
    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    class PaymentMethod(models.TextChoices):
        CASH = ('cash', _('Cache'))
        NON_CASH = ('non_cash', _('Non_cash'))

    company_name = models.CharField(max_length=255, verbose_name='название компании')
    bin_iin = models.PositiveBigIntegerField(verbose_name='БИН/ИИН')
    iik = models.CharField(max_length=255, verbose_name='ИИК')
    bank = models.CharField(max_length=255, verbose_name='IBAN')
    bik = models.CharField(max_length=255, verbose_name='БИК')
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.NON_CASH,
        verbose_name='способ оплаты'
    )
    contact_person = models.ForeignKey(ContactPersonModel, on_delete=models.CASCADE, verbose_name='контактное лицо')
    loyalty = models.ForeignKey(
        LoyaltyModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Уровень системы лояльности'
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = 'company'
        super().save(*args, **kwargs)