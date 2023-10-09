from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from apps.user.validators import validate_phone_number


class RegionModel(models.Model):
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)


class BaseUserModel(AbstractUser):
    class Meta:
        verbose_name = 'Базовый Пользователь'
        verbose_name_plural = 'Базовые Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    last_name = None
    first_name = None
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[validate_phone_number])
    email = models.EmailField(unique=True)
    region = models.ForeignKey(RegionModel, on_delete=models.CASCADE, null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse('')


class AddressModel(models.Model):
    district = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    house_number = models.CharField(max_length=255, blank=True, null=True)
    apartment_number = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, null=True)

