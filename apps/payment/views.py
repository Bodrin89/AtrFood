from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.order.models import Order
from apps.payment.serializers import PaymentSerializer
from config.settings import LOGGER


class PaymentView(CreateAPIView):
    """Отправка платежа"""
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
