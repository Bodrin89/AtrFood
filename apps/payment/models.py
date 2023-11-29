from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.order.models import Order
from apps.user.models import BaseUserModel


class PaymentOrder(models.Model):
    """Модель заказа сформированного на оплату"""

    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name='payment_user')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_order')
    event = models.CharField(max_length=255, verbose_name=_('платежное событие'))
    payment_order_id = models.CharField(max_length=255, verbose_name=_('id заказа в системе оплаты'))
    status = models.CharField(max_length=255, verbose_name=_('статус платежа'))
    created_at = models.DateTimeField(verbose_name=_('дата создания заказа в системе оплаты'))
    amount = models.CharField(
        max_length=255,
        help_text='Сумма указывается с сотыми долями, пример: 100 тенге указывается как 10000',
        verbose_name=_('сумма'))
    display_amount = models.CharField(
        max_length=255,
        help_text='Сумма указывается с сотыми долями, пример: 100 тенге указывается как 10000',
        verbose_name=_('отображаемая сумма'))
    currency = models.CharField(max_length=255, verbose_name=_('валюта'))
