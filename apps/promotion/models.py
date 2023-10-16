from django.db import models

from apps.product.models import CategoryProductModel, ProductModel
from django.utils.translation import gettext_lazy as _


class Gift(models.Model):
    """Модель подарков"""
    class Meta:
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'

    name = models.CharField(max_length=255, verbose_name='Название подарка')
    description = models.TextField(blank=True, null=True, verbose_name='Описание подарка')


class DiscountModel(models.Model):
    """Модель конструктора акций"""
    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    ACTION_TYPE_CHOICES = [
        ('discount', _('Скидка')),
        ('gift', _('Подарок')),
    ]

    name = models.CharField(max_length=255, verbose_name="Наименование акции")
    category_product = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE,
                                         verbose_name="Категория товара")
    product = models.ManyToManyField(ProductModel, related_name='products', verbose_name="товары по акции")
    use_limit_sum_product = models.BooleanField(default=True, verbose_name="Учитывать лимит по сумме товара в корзине")
    limit_sum_product = models.FloatField(default=0, verbose_name="Сумма товара в корзине после которой действует "
                                                                  "акция")
    count_person = models.PositiveIntegerField(default=0, verbose_name="количество человек воспользовавшихся акцией")
    count_product = models.PositiveIntegerField(default=0, verbose_name="количество купленных товаров по акции")
    use_limit_person = models.BooleanField(default=True, verbose_name="Учитывать лимит по количеству человек")
    limit_person = models.PositiveIntegerField(verbose_name="Ограничение по количеству человек")
    use_limit_product = models.BooleanField(default=True, verbose_name="Учитывать лимит по количеству товара")
    limit_product = models.PositiveIntegerField(verbose_name="Ограничение по количеству товара")
    use_limit_loyalty = models.BooleanField(default=True, verbose_name="Учитывать систему лояльности")
    date_end_discount = models.DateField(verbose_name="Дата окончания акции")
    is_active = models.BooleanField(default=False, verbose_name="Действующая/архивная акция")
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES, verbose_name='Тип акции')
    discount_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Размер скидки')
    gift = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Подарок')


class LoyaltyModel(models.Model):
    """Модель системы лояльности"""
    class Meta:
        verbose_name = 'Система лояльности'
        verbose_name_plural = 'Системы лояльности'

    LEVEL_LOYALTY = [
            ('bronze', _('бронза')),
            ('silver', _('серебро')),
            ('gold', _('золото')),
            ('platinum', _('платина')),
    ]

    level = models.CharField(max_length=10, choices=LEVEL_LOYALTY, verbose_name="Уровень лояльности")
    discount_percentage = models.PositiveSmallIntegerField(verbose_name="Процент скидки")
    sum_step = models.PositiveIntegerField(verbose_name="Порог цены")
