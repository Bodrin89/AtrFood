from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cart.models import CartModel, CartItem
from apps.cart.serializers import CreateCartSerializer, ListCartSerializer
from apps.cart.services import ServiceCart
from apps.product.models import ProductModel
from config.settings import LOGGER


class CreateCartView(CreateAPIView):
    """Добавление товара в корзину"""
    serializer_class = CreateCartSerializer
    queryset = CartModel.objects.all()

    def perform_create(self, serializer):
        product_item = self.request.data.get('product_item')
        cart_id = self.request.data.get('cart_id')
        serializer.save(product_item=product_item, cart_id=cart_id)


class ListCartView(RetrieveAPIView):
    """Получение всех товаров из корзины и их количества в заказе"""
    serializer_class = ListCartSerializer

    def get_queryset(self):
        cart_id = self.kwargs.get('pk')
        product_cart = CartModel.objects.filter(id=cart_id)
        return product_cart


class DeleteProductCartView(DestroyAPIView):
    """Удаление товара из корзины"""
    def delete(self, request, *args, **kwargs):
        cart_id = self.request.data.get('cart_id')
        cart_item_id = self.request.data.get('cart_item_id')
        del_obj = CartItem.objects.filter(id=cart_item_id, cart_id=cart_id)
        del_obj.delete()
        ServiceCart.get_total_sum(cart_id)
        return Response('Объект удален')

#
# class TotalSumProduct(APIView):
#     """Получение общей суммы в корзине и проверка товара на наличие"""
#     def get(self, request, *args, **kwargs):
#         return ServiceCart.get_total_sum(request)
