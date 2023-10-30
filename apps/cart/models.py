from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.product.models import ProductModel


class CartModel(models.Model):
    """Корзина"""
    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Товар'))
    quantity_product = models.IntegerField(verbose_name=_('Выбор количества товара'))
    sum_products = models.FloatField(verbose_name=_('Сумма по товару в корзине'))
    total_price = models.FloatField(verbose_name=_('Итоговая сумма всех товаров'))
