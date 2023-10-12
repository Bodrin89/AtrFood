from django.db import models

from apps.product.models import ProductModel


class CartModel(models.Model):
    """Корзина"""
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="товар")
    quantity_product = models.IntegerField(verbose_name="выбор количества товара")
    sum_products = models.FloatField(verbose_name="сумма товаров в корзине")
