from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.cart.models import CartModel, CartItem
from apps.cart.services import ServiceCart
from apps.product.models import ProductModel
from apps.product.serializers import ProductInfoSerializer, GiftInfoSerializer
from config.settings import LOGGER


class CreateCartSerializer(serializers.ModelSerializer):
    """Добавление товара в корзину"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartModel
        fields = ('id', 'user')

    # def validate_quantity_product(self, value):
    #     """Проверка, что quantity_product больше 0"""
    #     if value <= 0:
    #         raise serializers.ValidationError(_('Количество товара должно быть больше 0'))
    #     return value

    def create(self, validated_data):
        return ServiceCart.add_cart(validated_data)


class CartProductInfoSerializer(serializers.ModelSerializer):
    """Сериализатор информации о товаре в корзине"""

    class Meta:
        model = ProductModel
        fields = ('id', 'name', 'price', 'opt_price', 'article', 'discount_price', 'rating', 'existence', 'images')


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductInfoSerializer(read_only=True)
    gifts = GiftInfoSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'quantity_product', 'sum_products', 'product', 'gifts')


class ListCartSerializer(serializers.ModelSerializer):
    """Получение всех товаров из корзины и их количества в заказе"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_item = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = CartModel
        fields = ('id', 'total_price', 'user', 'cart_item')

