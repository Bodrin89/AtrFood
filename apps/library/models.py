from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.user.validators import validate_phone_number


class Region(models.Model):
    class Meta:
        verbose_name = _('Область')
        verbose_name_plural = _('Области')
    name = models.CharField(max_length=255, verbose_name=_('Область'))

    def __str__(self):
        return f'{self.name}'


class City(models.Model):
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

    name = models.CharField(max_length=255, verbose_name=_('Город'))
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='city', null=True, verbose_name=_('Область'))

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
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='district', null=True, verbose_name=_('Город') )

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


class AddressArtFood(models.Model):
    class Meta:
        verbose_name = _('Адрес магазина ArtFood')
        verbose_name_plural = _('Адреса магазинов ArtFood')

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_("Город"))
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_("Район"))
    street = models.CharField(max_length=255, verbose_name=_("Улица"))
    house_number = models.CharField(max_length=255, verbose_name=_("Номер дома"))
    office_number = models.PositiveSmallIntegerField(verbose_name=_("Номер офиса"), null=True, blank=True)

    url = models.URLField(verbose_name=_("Поле для ссылки"))


class OpenStore(models.Model):
    class Meta:
        verbose_name = _('Режим работы магазина')
        verbose_name_plural = _('Режимы работы магазинов')

    class DayWeek(models.TextChoices):
        MONDAY = (1, _("Понедельник"))
        TUESDAY = (2, _("Вторник"))
        WEDNESDAY = (3, _("Среда"))
        THURSDAY = (4, _("Четверг"))
        FRIDAY = (5, _("Пятница"))
        SATURDAY = (6, _("Суббота"))
        SUNDAY = (7, _("Воскресенье"))

    day = models.CharField(max_length=1, choices=DayWeek.choices, default=DayWeek.MONDAY, verbose_name=_("День недели"))
    time_open = models.TimeField(verbose_name=_("Время открытия"), null=True)
    time_close = models.TimeField(verbose_name=_("Время закрытия"), null=True)
    address = models.ForeignKey(AddressArtFood, on_delete=models.CASCADE, verbose_name=_("Адрес магазина"))


class ContactArtFood(models.Model):
    class Meta:
        verbose_name = _('Контакт компании')
        verbose_name_plural = _('Контакты компаний')

    phone_numbers = models.CharField(max_length=20, validators=[validate_phone_number],
                                     verbose_name=_('Номер телефона'))
    address = models.ForeignKey(AddressArtFood, on_delete=models.CASCADE, verbose_name=_("Адрес магазина"), null=True)


class SocialNetwork(models.Model):
    class Meta:
        verbose_name = _('Социальная сеть')
        verbose_name_plural = _('Социальные сети')

    name = models.CharField(max_length=255, verbose_name=_("Название социальной сети"))
    url_network = models.URLField(verbose_name=_("Ссылка на социальную сеть"))

