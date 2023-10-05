from django.contrib.auth.models import AbstractUser
from django.db import models


class RegionModel(models.Model):
    region = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)


class AddressModel(models.Model):
    district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)
    apartment_number = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)


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
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(RegionModel, on_delete=models.CASCADE, null=True)


class IndividualUserModel(BaseUserModel):
    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'

    second_phone_number = models.CharField(max_length=20, null=True, blank=True)


class ContactPersonModel(models.Model):
    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'

    surname = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)


class CompanyUserModel(BaseUserModel):
    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличные'
        NON_CASH = 'non_cash', 'Безналичный расчет'

    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    bin_iin = models.CharField(max_length=255)
    iik = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    bik = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.NON_CASH)
    contact_person = models.ForeignKey(ContactPersonModel, on_delete=models.CASCADE)

