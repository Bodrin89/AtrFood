from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

    name = models.CharField(max_length=255, verbose_name=_('Город'))

    def __str__(self):
        return f'{self.name}'


class CountryManufacturer(models.Model):
    class Meta:
        verbose_name = _('Страна производства')
        verbose_name_plural = _('Страны производства')

    name = models.CharField(max_length=255, verbose_name=_('Страна производства'))

    def __str__(self):
        return f'{self.name}'


class District(models.Model):
    class Meta:
        verbose_name = _('Район')
        verbose_name_plural = _('Районы')

    name = models.CharField(max_length=255, verbose_name=_('Район'))

    def __str__(self):
        return f'{self.name}'


class ManufacturingCompany(models.Model):
    class Meta:
        verbose_name = _('Компания производитель')
        verbose_name_plural = _('Компании производители')

    name = models.CharField(max_length=255, verbose_name=_('Компания производитель'))
    logo = models.ImageField(upload_to='logo/', verbose_name=_('Логотип'), blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class NameLevelLoyalty(models.Model):
    class Meta:
        verbose_name = _('Наименование уровня лояльности')
        verbose_name_plural = _('Наименование уровней лояльности')

    name = models.CharField(max_length=255, verbose_name=_('Наименование уровня лояльности'))

    def __str__(self):
        return f'{self.name}'


class PackageType(models.Model):
    class Meta:
        verbose_name = _('Тип упаковки')
        verbose_name_plural = _('Тип упаковок')

    name = models.CharField(max_length=255, verbose_name=_('Тип упаковки'))

    def __str__(self):
        return f'{self.name}'


class ReturnPolicy(models.Model):
    class Meta:
        verbose_name = _('Условие возврата')
        verbose_name_plural = _('Условия возврата')

    name = models.TextField(verbose_name=_('Условие возврата'))

    def __str__(self):
        return f'{self.id}'


class PrivacyPolicy(models.Model):
    class Meta:
        verbose_name = _('Политика конфиденциальности')
        verbose_name_plural = _('Политика конфиденциальности')

    name = models.TextField(verbose_name=_('политика конфиденциальности'))

    def __str__(self):
        return f'{self.id}'


class AboutCompany(models.Model):
    class Meta:
        verbose_name = _('О комании')
        verbose_name_plural = _('О комании')

    name = models.TextField(verbose_name=_('О комании'))

    def __str__(self):
        return f'{self.id}'
