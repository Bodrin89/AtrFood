from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from apps.order.models import Order, OrderItem
from apps.product.models import ProductModel
from rest_framework.exceptions import ValidationError


class ServiceOrder:
    @staticmethod
    def create_order(validated_data):
        user = validated_data['request'].user
        cart = validated_data['session'].get('product_cart')
        session = validated_data['session']
        if not cart:
            raise ValidationError({'error': 'Корзина пуста'}, code=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(
            user=user,
            payment_method=validated_data.get('payment_method'),
            delivery_address=validated_data.get('delivery_address'),
            contact_phone=validated_data.get('contact_phone'),
        )
        for item in cart:
            try:
                product = ProductModel.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity_product'],
                    price=item['sum_products'],
                )
            except ObjectDoesNotExist:
                raise ValidationError(
                    {'error': f"Продукт с ID {item['product_id']} не найден"},
                    code=status.HTTP_400_BAD_REQUEST
                )

        order.save()
        session['product_cart'] = []
        session.modified = True
        return order
