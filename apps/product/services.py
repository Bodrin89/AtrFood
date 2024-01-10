
from apps.product.models import (
                                 FavoriteProductModel,
                                 ProductModel,)
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from config.settings import LOGGER


class ServiceProduct:

    @staticmethod
    def _calculation_discount(price: int, discount: int) -> float:
        """Расчет цены с учетом скидки"""
        result_price = price - (price * discount) / 100
        return result_price

    @staticmethod
    def _calculation_existence(quantity_stock: int, quantity_select: int = 0) -> bool:
        """Расчет наличия товара на складе (есть/нет)"""
        if quantity_stock - quantity_select > 0:
            return True
        return False

    @staticmethod
    def add_delete_product_favorite(validated_data: dict):
        """Добавление товара в избранное"""
        user = validated_data['user']
        ids = validated_data['ids']
        if not ids:
            raise serializers.ValidationError({'error': _('Список товаров пуст')})

        favorite_products = []

        for product_id in ids:
            try:
                product = ProductModel.objects.get(id=product_id)
                favorite_product, created = FavoriteProductModel.objects.get_or_create(product=product)
                favorite_product.user.add(user)
                favorite_products.append(favorite_product)
            except ProductModel.DoesNotExist:
                favorite_products.append({'product_id': product_id, 'error': _('Товар не найден')})
        return favorite_products
