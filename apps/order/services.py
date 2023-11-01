from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.order.models import Order, OrderItem, DeliveryAddress
from apps.clients.models import AddressModel
from apps.product.models import ProductModel
from config.settings import LOGGER


class ServiceOrder:
    @staticmethod
    def create_order(validated_data):
        user = validated_data['request'].user
        cart = validated_data['session'].get('product_cart')
        session = validated_data['session']

        if not cart:
            raise ValidationError({'error': _('Корзина пуста')}, code=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(
            user=user,
            payment_method=validated_data.get('payment_method'),
            contact_phone=validated_data.get('contact_phone'),
        )
        selected_address = validated_data.get('delivery_address')
        delivery_data = AddressModel.objects.get(id=selected_address.id)
        DeliveryAddress.objects.create(
            city=delivery_data.city,
            district=delivery_data.district,
            street=delivery_data.street,
            house_number=delivery_data.house_number,
            apartment_number=delivery_data.apartment_number,
            floor=delivery_data.floor,
            order=order
        )

        for item in cart:
            try:
                gift_item = item['gifts']
                gift = None
                if gift_item:
                    gift_id = gift_item[0]['id']
                    gift = ProductModel.objects.get(id=gift_id)

                product = ProductModel.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity_product'],
                    price=item['sum_products'],
                    gift=gift
                )
            except ObjectDoesNotExist:
                raise ValidationError(
                    {'error': _(f"Продукт с ID") + f" {item['product_id']} " + _("не найден")},
                    code=status.HTTP_400_BAD_REQUEST
                )

        order.save()
        session['product_cart'] = []
        session.modified = True
        return order
