from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.payment.serializers import PaymentSerializer, HandlingStatusPayment


class PaymentView(CreateAPIView):
    """Отправка платежа"""
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer


class WebhookIoka(CreateAPIView):
    """Webhook подтверждения оплаты"""
    serializer_class = HandlingStatusPayment



