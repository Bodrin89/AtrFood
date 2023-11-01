from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.promotion.models import LoyaltyModel
from apps.user.models import BaseUserModel
from apps.library.models import City, CountryManufacturer, District


class ContactPersonModel(models.Model):
    class Meta:
        verbose_name = _('Контактное лицо')
        verbose_name_plural = _('Контактные лица')

    surname = models.CharField(max_length=255, verbose_name=_('фамилия'))
    first_name = models.CharField(max_length=255, verbose_name=_('имя'))
    second_name = models.CharField(max_length=255, verbose_name=_('отчество'))
    user = models.OneToOneField(
        BaseUserModel,
        on_delete=models.CASCADE,
        related_name='contact_person',
        null=True,
        verbose_name=_('Контактное лицо')
    )

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.second_name}'


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
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.NON_CASH,
                                      verbose_name=_('способ оплаты'))
    loyalty = models.ForeignKey(LoyaltyModel, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                verbose_name=_('Уровень системы лояльности'))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = 'company'
        super().save(*args, **kwargs)


class CompanyAddress(models.Model):
    class Meta:
        verbose_name = _('Адрес Компании')
        verbose_name_plural = _('Адреса компаний')

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('Город'))
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_('Район'), blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Улица'))
    house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Номер дома'))
    office_number = models.PositiveSmallIntegerField(verbose_name=_('Номер офиса'))
    user = models.OneToOneField(
        BaseUserModel,
        on_delete=models.CASCADE,
        related_name='company_address',
        null=True,
        verbose_name=_('Пользователи')
    )

    def __str__(self):
        return f'{self.city}'
