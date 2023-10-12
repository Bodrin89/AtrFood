from rest_framework import serializers

from apps.cart.models import CartModel
from apps.cart.services import ServiceCart
from apps.product.models import ProductModel
from config.settings import LOGGER


class CreateCartSerializer(serializers.ModelSerializer):
    """Добавление товара в корзину"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartModel
        fields = ('quantity_product', 'user')

    def create(self, validated_data):
        return ServiceCart.add_cart(validated_data)


class ListCartSerializer(serializers.Serializer):
    """Получение всех товаров из корзины и их количества в заказе"""

    product_id = serializers.IntegerField()
    quantity_product = serializers.IntegerField(min_value=0)
    sum_products = serializers.FloatField(min_value=0.0)
    total_price = serializers.FloatField(min_value=0.0)

    def to_representation(self, instance):
        return ServiceCart.get_list_product_cart(instance)
