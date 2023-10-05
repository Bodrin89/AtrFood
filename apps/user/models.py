from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.user.validators import validate_phone_number


class RegionModel(models.Model):
    region = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)


class BaseUserModel(AbstractUser):
    class Meta:
        verbose_name = 'Базовый Пользователь'
        verbose_name_plural = 'Базовые Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    last_name = None
    first_name = None
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[validate_phone_number])
    email = models.EmailField(unique=True)
    region = models.ForeignKey(RegionModel, on_delete=models.CASCADE, null=True)


class AddressModel(models.Model):
    district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)
    apartment_number = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, null=True)
