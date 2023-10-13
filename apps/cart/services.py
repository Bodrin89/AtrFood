from rest_framework import status
from rest_framework.response import Response

from apps.product.models import ProductModel
from config.settings import LOGGER


class ServiceCart:

    @staticmethod
    def get_sum_price_product(price, quantity_product, discount_amounts):
        """Расчет суммы товаров в корзине с учетом всех скидок"""
        return (price - (price * sum(discount_amounts)) / 100) * quantity_product

    @staticmethod
    def add_cart(validated_data: dict) -> dict:
        """Сохранение товаров в корзину в сессии"""

        product_id = validated_data['product_id']
        session = validated_data['session']
        product_cart = session.get('product_cart', [])
        product: ProductModel = validated_data['product']
        price = ProductModel.objects.get(id=product_id).price


        discounts = product.discountmodel_set.all().filter(is_active=True)
        discount_amounts = [discount.discount_amount for discount in discounts]

        try:
            ProductModel.objects.get(id=product_id, existence=True)
        except ProductModel.DoesNotExist:
            raise Exception("Товара нет в наличии")

        found = False

        for item in product_cart:
            if item.get('product_id') == product_id:
                item['quantity_product'] = validated_data['quantity_product']
                item['sum_products'] = ServiceCart.get_sum_price_product(price, validated_data['quantity_product'],
                                                                         discount_amounts)
                found = True
                break

        if not found:
            product_cart.append({
                'product_id': product_id,
                'quantity_product': validated_data['quantity_product'],
                'sum_products': ServiceCart.get_sum_price_product(price, validated_data['quantity_product'],
                                                                  discount_amounts)
            })

        session['product_cart'] = product_cart
        session.modified = True
        return validated_data

    @staticmethod
    def get_list_product_cart(instance):
        """Получение всех товаров из корзины и их количества в заказе"""
        product_id = instance['product_id']
        quantity_product = instance['quantity_product']
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

    @staticmethod
    def get_total_sum(request):
        """Получение общей суммы в корзине и проверка товара на наличие"""

        product_cart = request.session.get('product_cart', [])
        total_sum = []
        not_existence = []
        for item in product_cart:
            product = ProductModel.objects.get(id=item.get('product_id'))
            if product.existence is True:
                total_sum.append(item.get('sum_products'))
            else:
                not_existence.append(product.id)
        return Response({'total_sum': sum(total_sum), "Товары не в наличии": not_existence})

        # if validated_data['user'].id:
        #     LOGGER.debug(validated_data)
        #
        # return CartModel.objects.create()
