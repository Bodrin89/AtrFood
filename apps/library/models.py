from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

    name = models.CharField(max_length=255, verbose_name=_('Город'))

    def __str__(self):
        return self.name


class Region(models.Model):
    class Meta:
        verbose_name = _('Область')
        verbose_name_plural = _('Области')

    name = models.CharField(max_length=255, verbose_name=_('Область'))

    def __str__(self):
        return self.name


class District(models.Model):
    class Meta:
        verbose_name = _('Район')
        verbose_name_plural = _('Районы')

    name = models.CharField(max_length=255, verbose_name=_('Район'))

    def __str__(self):
        return self.name


class ManufacturingCompany(models.Model):
    class Meta:
        verbose_name = _('Компания производитель')
        verbose_name_plural = _('Компании производитель')

    name = models.CharField(max_length=255, verbose_name=_('Компания производитель'))

    def __str__(self):
        return self.name


class ManufacturingCountry(models.Model):
    class Meta:
        verbose_name = _('Страна производитель')
        verbose_name_plural = _('Страны производители')

    name = models.CharField(max_length=255, verbose_name=_('Страна производитель'))

    def __str__(self):
        return self.name


class NameLevelLoyalty(models.Model):
    class Meta:
        verbose_name = _('Наименование уровня лояльности')
        verbose_name_plural = _('Наименование уровней лояльности')

    name = models.CharField(max_length=255, verbose_name=_('Страна производитель'))

    def __str__(self):
        return self.name







