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

    class TimeZone(models.TextChoices):
        Almaty = ('Asia/Almaty', 'Asia/Almaty')
        Aqtobe = ('Asia/Aqtobe', 'Asia/Aqtobe')

    name = models.CharField(max_length=255, verbose_name=_('Город'))
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='city',
                               null=True, verbose_name=_('Область'))
    timezone = models.CharField(max_length=50, choices=TimeZone.choices, default=TimeZone.Almaty,
                                verbose_name=_('Часовой пояс города'))

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

    url = models.URLField(null=True, blank=True, verbose_name=_("Поле для ссылки"))

    def __str__(self):
        return f'Город: {self.city}, район: {self.district}'


class OpenStore(models.Model):
    class Meta:
        verbose_name = _('Режим работы магазина')
        verbose_name_plural = _('Режимы работы магазинов')

    class DayWeek(models.TextChoices):
        MONDAY = ("Понедельник", _("Понедельник"))
        TUESDAY = ("Вторник", _("Вторник"))
        WEDNESDAY = ("Среда", _("Среда"))
        THURSDAY = ("Четверг", _("Четверг"))
        FRIDAY = ("Пятница", _("Пятница"))
        SATURDAY = ("Суббота", _("Суббота"))
        SUNDAY = ("Воскресенье", _("Воскресенье"))

    day = models.CharField(max_length=11, choices=DayWeek.choices, default=DayWeek.MONDAY,
                           verbose_name=_("День недели"))
    time_open = models.TimeField(verbose_name=_("Время открытия"), null=True)
    time_close = models.TimeField(verbose_name=_("Время закрытия"), null=True)
    address = models.ForeignKey(AddressArtFood, related_name='open_store', on_delete=models.CASCADE,
                                verbose_name=_("Адрес магазина"))

    def __str__(self):
        return f'Режим работы магазина'


class ContactArtFood(models.Model):
    class Meta:
        verbose_name = _('Контакт компании')
        verbose_name_plural = _('Контакты компаний')

    phone_numbers = models.CharField(max_length=20, validators=[validate_phone_number],
                                     verbose_name=_('Номер телефона'))
    address = models.ForeignKey(AddressArtFood, on_delete=models.CASCADE, related_name='contact_store',
                                verbose_name=_("Адрес магазина"), blank=True, null=True)

    def __str__(self):
        return f'{self.phone_numbers}'


class SocialNetwork(models.Model):
    class Meta:
        verbose_name = _('Социальная сеть')
        verbose_name_plural = _('Социальные сети')

    name = models.CharField(max_length=255, verbose_name=_("Название социальной сети"))
    url_network = models.URLField(verbose_name=_("Ссылка на социальную сеть"))

    def __str__(self):
        return f'{self.name}'


class PolicyPaymentDelivery(models.Model):
    class Meta:
        verbose_name = _('Условие оплаты и доставки')
        verbose_name_plural = _('Условия оплаты и доставки')

    text = models.TextField()

    def __str__(self):
        return f'{self.id}'
