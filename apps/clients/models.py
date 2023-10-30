from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.user.models import BaseUserModel
from apps.library.models import City, Country, District
from django.utils.translation import gettext_lazy as _


class AddressModel(models.Model):
    class Meta:
        verbose_name = _('Адрес')
        verbose_name_plural = _('Адреса')

    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Страна'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('Город'))
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_('Район'), blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Улица'))
    house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Номер дома'))
    apartment_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Номер квартиры'))
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Этаж'))
    user = models.ForeignKey(
        BaseUserModel,
        on_delete=models.CASCADE,
        related_name='addresses',
        null=True,
        verbose_name=_('Пользователь')
    )

    def __str__(self):
        return f'{self.district}, {self.street}'


@receiver(pre_save, sender=AddressModel)
def limit_addresses_per_user(sender, instance, **kwargs):
    if instance.user:
        existing_addresses = AddressModel.objects.filter(user=instance.user).count()

        if instance.pk:
            if existing_addresses > 3:
                raise ValidationError('У пользователя не может быть больше 3 адресов.')
        else:
            if existing_addresses >= 3:
                raise ValidationError('У пользователя не может быть больше 3 адресов.')