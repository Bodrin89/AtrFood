from rest_framework import serializers

from apps.payment.models import PaymentOrder
from apps.payment.services import PaymentService
from config.settings import LOGGER


class PaymentSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_id = serializers.CharField(max_length=255, write_only=True)
    pay_url = serializers.URLField(read_only=True)

    def create(self, validated_data):
        """Создание заказа на оплату и получение ссылки для оплаты"""
        return PaymentService.create_payment_order(validated_data)


class HandlingStatusPayment(serializers.ModelSerializer):
    """Обработка статуса платежа"""
    status = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = PaymentOrder
        fields = ('event', 'status',)

    def validate(self, attrs):
        data = self.initial_data
        if data.get('event') and data.get('order'):
            return self.initial_data
        raise serializers.ValidationError({'error': 'не верные данные'})

    def create(self, validated_data):
        payment_order = PaymentService.proof_payment(validated_data)
        return payment_order
