from rest_framework import serializers
from apps.order.models import Order, OrderItem
from apps.order.services import ServiceOrder
from apps.product.serializers import ProductInfoSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор товаров заказа"""
    product = ProductInfoSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    """Сериализатор создания заказа"""
    class Meta:
        model = Order
        fields = ('payment_method', 'delivery_address', 'contact_phone')

    def create(self, validated_data):
        return ServiceOrder.create_order(validated_data)


class GetOrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказов пользователя"""

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'payment_method',
            'date_created',
            'delivery_address',
            'contact_phone',
            'status',
            'total_quantity',
            'total_price',
            'items',
            ]
