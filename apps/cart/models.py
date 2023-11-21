from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.product.models import ProductModel
from apps.promotion.models import Gift
from apps.user.models import BaseUserModel


class CartModel(models.Model):
    """Корзина"""
    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')

    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name='cart_user', null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True, verbose_name=_('Итоговая сумма всех товаров'))


class CartItem(models.Model):
    """Единица товара в корзине"""
    class Meta:
        verbose_name = _('Единица товара в корзине')
        verbose_name_plural = _('Единицы товаров в корзине')
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='cart_item', verbose_name=_('Корзина'))
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='cart', verbose_name=_('Товар'))
    quantity_product = models.IntegerField(verbose_name=_('Выбор количества товара'))
    sum_products = models.FloatField(verbose_name=_('Сумма по товару в корзине'))
    gifts = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='cart_gift',
                              verbose_name=_('Подарок'))

    def __str__(self):
        return f'CartItem c товаром {self.product.name} в корзине {self.cart.id}'

