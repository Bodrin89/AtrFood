from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.user.models import BaseUserModel
from apps.library.models import City, Country, District


class AddressModel(models.Model):
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name='Район', blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name='Улица')
    house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='Номер дома')
    apartment_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Номер квартиры')
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Этаж')
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name='addresses', null=True, verbose_name='Пользователь')

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