from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.user.models import BaseUserModel


class AddressModel(models.Model):
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    district = models.CharField(max_length=255, blank=True, null=True, verbose_name='район')
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name='улица')
    house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='номер дома')
    apartment_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='номер квартиры')
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='этаж')
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name='addresses', null=True, verbose_name='пользователь')

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