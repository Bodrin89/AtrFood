import os

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.order.models import Order
from dotenv import load_dotenv

load_dotenv()


class PaymentSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_id = serializers.CharField(max_length=255, write_only=True)
    amount = serializers.CharField(max_length=255, read_only=True)
    api_key = serializers.CharField(max_length=255, read_only=True)
    currency = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        """Создание данных для отправки на оплату"""
        user = validated_data['user']
        order_id = validated_data['order_id']
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            raise serializers.ValidationError(_('Заказ не найден'))
        total_price = order.total_price
        if total_price:
            total_price = str(total_price) + '00'

        body = {
            "amount": total_price,
            "api_key": os.getenv('PAYMENT_API_KEY'),
            "currency": "KZT",
        }
        return body

