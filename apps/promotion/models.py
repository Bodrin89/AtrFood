from itertools import chain

from django.db import models
from django.db.models import Q, F
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.product.models import CategoryProductModel, ProductModel
from config.settings import LOGGER


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

    name = models.CharField(max_length=255, verbose_name='Наименование акции')
    category_product = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE,
                                         verbose_name='Категория товара')
    product = models.ManyToManyField(ProductModel, related_name='products', verbose_name='товары по акции')
    use_limit_sum_product = models.BooleanField(default=True, verbose_name='Учитывать лимит по сумме товара в корзине')
    limit_sum_product = models.FloatField(default=0, verbose_name='Сумма товара в корзине после которой действует '
                                                                  'акция')
    count_person = models.PositiveIntegerField(default=0, verbose_name='количество человек воспользовавшихся акцией')
    count_product = models.PositiveIntegerField(default=0, verbose_name='количество купленных товаров по акции')
    use_limit_person = models.BooleanField(default=True, verbose_name='Учитывать лимит по количеству человек')
    limit_person = models.PositiveIntegerField(verbose_name='Ограничение по количеству человек')
    use_limit_product = models.BooleanField(default=True, verbose_name='Учитывать лимит по количеству товара')
    limit_product = models.PositiveIntegerField(verbose_name='Ограничение по количеству товара')
    use_limit_loyalty = models.BooleanField(default=True, verbose_name='Учитывать систему лояльности')
    date_end_discount = models.DateField(verbose_name='Дата окончания акции')
    is_active = models.BooleanField(default=False, verbose_name='Действующая/архивная акция')
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

    level = models.CharField(max_length=10, choices=LEVEL_LOYALTY, verbose_name='Уровень лояльности')
    discount_percentage = models.PositiveSmallIntegerField(verbose_name='Процент скидки')
    sum_step = models.PositiveIntegerField(verbose_name='Порог цены')


prod = DiscountModel.objects.all()

@receiver(post_save, sender=DiscountModel)
def apply_discount_to_products(sender, instance, created, **kwargs):
    """Обработчик события создания скидки"""
    change_discount_price(prod)


@receiver(m2m_changed, sender=DiscountModel.product.through)
def update_discount_price(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Обработчик события изменения скидки при удалении какого-то продукта из скидки"""
    change_discount_price(prod)
    if action == 'post_remove':
        removed_products = ProductModel.objects.filter(pk__in=pk_set)
        not_remove_product = []
        for discount in prod:
            products = discount.product.all()
            not_remove_product.append(products)
        a = [item for sublist in not_remove_product for item in sublist]
        for item in removed_products:
            if item not in a:
                item.discount_price = item.price
                item.save()


def change_discount_price(prod):
    """Изменение цены со скидкой"""
    for discount in prod:
        products = discount.product.all()
        for product in products:
            quantity_product = 1
            limit_sum_product = 1.0
            discounts = get_discount(product, quantity_product, limit_sum_product)
            discount_amounts = [discount.discount_amount for discount in discounts]
            product.discount_price = get_sum_price_product(product.price, quantity_product, discount_amounts)
            product.save()

def get_discount(product: ProductModel, quantity_product: int, limit_sum_product: float) -> list[DiscountModel]:
    """Фильтр акций по условиям"""
    discounts = product.products.all().filter(
        Q(is_active=True) &
        (Q(use_limit_person=True, count_person__lt=F('limit_person')) | ~Q(use_limit_person=True)) &
        (Q(use_limit_product=True, limit_product__gt=F('count_product') + quantity_product) | ~Q(
            use_limit_product=True)) &
        (Q(use_limit_sum_product=True, limit_sum_product__lt=limit_sum_product) | ~Q(use_limit_sum_product=True))
    )
    return discounts


def get_sum_price_product(price, quantity_product, discount_amounts):
    """Расчет суммы товаров в корзине с учетом всех скидок"""
    return (price - (price * sum(discount_amounts)) / 100) * quantity_product
