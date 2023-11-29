from rest_framework import serializers

from apps.cart.serializers import CartProductInfoSerializer
from apps.order.models import Order, OrderItem, DeliveryAddress
from apps.order.services import ServiceOrder
from apps.product.serializers import ProductInfoSerializer, GiftInfoSerializer
from apps.clients.models import AddressModel
from apps.library.serializers import CitySerializer, DistrictSerializer
from config.settings import LOGGER


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор товаров заказа"""
    product = ProductInfoSerializer()
    gift = GiftInfoSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class DeliveryAddressSerializer(serializers.ModelSerializer):

    city = CitySerializer()
    district = DistrictSerializer()

    class Meta:
        model = DeliveryAddress
        fields = ('id', 'city', 'district', 'street', 'house_number', 'apartment_number', 'floor')
        read_only_fields = ['id', ]


class CreateOrderSerializer(serializers.ModelSerializer):
    """Сериализатор создания заказа"""
    delivery_method = serializers.BooleanField()
    delivery_address = serializers.PrimaryKeyRelatedField(
        queryset=AddressModel.objects.none(),
        required=True
    )

    class Meta:
        model = Order
        fields = ('payment_method', 'delivery_address', 'contact_phone', 'delivery_method')

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super(CreateOrderSerializer, self).__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields['delivery_address'].queryset = AddressModel.objects.filter(user=user)

    def create(self, validated_data):
        return ServiceOrder.create_order(validated_data)


class GetOrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказов пользователя"""

    order_items = OrderItemSerializer(many=True, read_only=True)
    delivery_address = DeliveryAddressSerializer(read_only=True)
    total_quantity = serializers.CharField(read_only=True)
    total_price = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    payment_method = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'payment_method',
            'date_created',
            'delivery_address',
            'contact_phone',
            'status',
            'total_quantity',
            'total_price',
            'order_items',
            ]

