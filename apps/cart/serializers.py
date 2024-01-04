from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.cart.models import CartModel, CartItem
from apps.cart.services import ServiceCart
from apps.product.models import ProductModel
from apps.product.serializers import ProductInfoSerializer, GiftInfoSerializer
from config.settings import LOGGER


class ProductItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity_product = serializers.IntegerField()


class CreateCartSerializer(serializers.ModelSerializer):
    """Добавление товара в корзину"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_id = serializers.IntegerField(required=False, read_only=True)
    product_item = ProductItemSerializer(many=True, write_only=True)

    class Meta:
        model = CartModel
        fields = ('id', 'user', 'cart_id', 'product_item')

    def validate(self, data):
        product_items = data.get('product_item', [])
        for item in product_items:
            quantity_product = item.get('quantity_product', 0)
            if quantity_product <= 0:
                raise serializers.ValidationError({'product_item': _('Количество товара должно быть больше 0.')})
        return data

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

