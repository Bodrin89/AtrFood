from django.contrib.auth.models import AbstractUser
from django.db import models


class RegionModel(models.Model):
    region = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)


class BaseUserModel(AbstractUser):
    class Meta:
        verbose_name = 'Базовый Пользователь'
        verbose_name_plural = 'Базовые Пользователи'

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    last_name = None
    first_name = None
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    region = models.ForeignKey(RegionModel, on_delete=models.SET_NULL, null=True)


class IndividualUserModel(BaseUserModel):
    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'

    second_phone_number = models.CharField(max_length=20, null=True, blank=True)


class CompanyUserModel(BaseUserModel):
    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    bin_iin = models.CharField(max_length=255)
    iik = models.CharField(max_length=255)
