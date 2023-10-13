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
    sum_product = models.FloatField(verbose_name="Сумма товара в корзине")
    count_person = models.PositiveIntegerField(default=0, verbose_name="количество человек воспользовавшихся акцией")
    count_product = models.PositiveIntegerField(default=0, verbose_name="количество купленных товаров по акции")
    limit_person = models.PositiveIntegerField(verbose_name="Ограничение по количеству человек")
    limit_product = models.PositiveIntegerField(verbose_name="Ограничение по количеству товара")
    date_end_discount = models.DateField(verbose_name="Дата окончания акции")
    is_active = models.BooleanField(default=False, verbose_name="Действующая/архивная акция")
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES, verbose_name='Тип акции')
    discount_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Размер скидки')
    gift = models.ForeignKey('Gift', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Подарок')
