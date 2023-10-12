from rest_framework import status
from rest_framework.response import Response

from apps.product.models import ProductModel
from config.settings import LOGGER


class ServiceCart:

    @staticmethod
    def add_cart(validated_data: dict) -> dict:
        """Сохранение товаров в корзину в сессии"""

        product_id = validated_data['product_id']
        session = validated_data['session']
        product_cart = session.get('product_cart', [])
        price = ProductModel.objects.get(id=product_id).price

        try:
            ProductModel.objects.get(id=product_id, existence=True)
        except ProductModel.DoesNotExist:
            raise Exception("Товара нет в наличии")

        found = False

        for item in product_cart:
            if item.get('product_id') == product_id:
                item['quantity_product'] = validated_data['quantity_product']
                item['sum_products'] = price * validated_data['quantity_product']
                found = True
                break

        if not found:
            product_cart.append({
                'product_id': product_id,
                'quantity_product': validated_data['quantity_product'],
                'sum_products': price * validated_data['quantity_product']
            })

        session['product_cart'] = product_cart
        session.modified = True
        return validated_data

    @staticmethod
    def get_list_product_cart(instance):
        """Получение всех товаров из корзины и их количества в заказе"""
        product_id = instance['product_id']
        quantity_product = instance['quantity_product']
        LOGGER.debug(instance)
        sum_products = instance['sum_products']

        try:
            product = ProductModel.objects.get(id=product_id)
            product_data = {
                'product_id': product_id,
                'quantity_product': quantity_product,
                'sum_products': sum_products,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                }
            }
        except ProductModel.DoesNotExist:
            product_data = {
                'product_id': product_id,
                'quantity_product': quantity_product,
                'product': None
            }
        return product_data

    @staticmethod
    def delete_product_cart(request, *args, **kwargs):
        """Удаление товара из корзины перезапись сессии"""
        product_cart = request.session.get('product_cart', [])
        product_id = kwargs.get('product_id')

        if not any(item.get('product_id') == product_id for item in product_cart):
            return Response({"message": 'Товар не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)

        updated_cart = [item for item in product_cart if item.get('product_id') != product_id]

        request.session['product_cart'] = updated_cart
        request.session.modified = True
        return Response({"message": 'Товар удален из корзины'}, status=status.HTTP_204_NO_CONTENT)


        # if validated_data['user'].id:
        #     LOGGER.debug(validated_data)
        #
        # return CartModel.objects.create()