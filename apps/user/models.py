from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from apps.user.validators import validate_phone_number


class RegionModel(models.Model):
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.region


class BaseUserModel(AbstractUser):
    class Meta:
        verbose_name = 'Базовый Пользователь'
        verbose_name_plural = 'Базовые Пользователи'

    USER_TYPES = (
        ('individual', 'Individual'),
        ('company', 'Company'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    last_name = None
    first_name = None
    phone_number = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        verbose_name="номер телефона"
        )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='individual')
    email = models.EmailField(unique=True, verbose_name="электронная почта")
    region = models.ForeignKey(
        RegionModel,
        on_delete=models.CASCADE,
        verbose_name="место положения область/город",
        null=True,
        blank=True
        )

    # def get_absolute_url(self):
    #     return reverse('')


class AddressModel(models.Model):
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    district = models.CharField(max_length=255, blank=True, null=True, verbose_name="район")
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name="улица")
    house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="номер дома")
    apartment_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="номер квартиры")
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="этаж")
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name='addresses', null=True, verbose_name="пользователь")

    def __str__(self):
        return self.district
