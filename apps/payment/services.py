import json
import os

import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.db import transaction

from apps.order.models import Order
from apps.payment.models import PaymentOrder
from config.settings import URL_PAYMENT_ORDER, CURRENCY, BACK_URL, LOGGER

API_KEY = os.getenv('PAYMENT_API_KEY')


class PaymentService:

    @staticmethod
    def create_payment_order(validated_data):
        """Создание или получение уже созданного заказа на оплату и получение ссылки для оплаты"""

        user = validated_data['user']
        order_id = validated_data['order_id']
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            raise serializers.ValidationError('Заказ не найден')
        total_price = order.total_price
        if total_price:
            total_price = str(total_price) + '00'

        body = json.dumps({'amount': total_price, "currency": CURRENCY, "back_url": BACK_URL})
        headers = {'API-KEY': API_KEY, 'Content-Type': 'application/json'}

        if get_payment_order := PaymentOrder.objects.filter(order_id=order_id).first():
            payment_order_id = get_payment_order.payment_order_id
            response = requests.get(URL_PAYMENT_ORDER + f'/{payment_order_id}', headers=headers, data=body)
            pay_url = response.json()['checkout_url']
            response_data = {"order_id": order_id, "pay_url": pay_url}
            return response_data
        else:
            response = requests.post(URL_PAYMENT_ORDER, headers=headers, data=body)

            with transaction.atomic():
                payment_order = response.json()['order']
                pay_url = payment_order['checkout_url']
                response_data = {"order_id": order_id, "pay_url": pay_url}
                created, _ = PaymentOrder.objects.get_or_create(user=user,
                                                                order=order,
                                                                payment_order_id=payment_order['id'],
                                                                status=payment_order['status'],
                                                                created_at=payment_order['created_at'],
                                                                amount=payment_order['amount'],
                                                                display_amount=payment_order['display_amount'],
                                                                currency=payment_order['currency'])
            return response_data

    @staticmethod
    def proof_payment(data: dict):
        """Подтверждение оплаты заказа и изменения его статуса"""
        data_order = data.get('order')
        payment_order_id = data_order['id']
        status = data_order['status']
        data_event = data.get('event')
        order_status = 'new_paid'
        if data_event != 'PAYMENT_CAPTURED':
            order_status = 'new_unpaid'
        try:
            with transaction.atomic():
                payment_order = PaymentOrder.objects.select_related('order').get(payment_order_id=payment_order_id)
                payment_order.event = data_event
                payment_order.status = status
                payment_order.order.status = order_status
                payment_order.order.save()
                payment_order.save()
                return payment_order
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError({"error": e})
        except Exception as e:
            raise serializers.ValidationError({"error": e})
