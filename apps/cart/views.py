from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from apps.cart.models import CartModel
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
    """Удаление товара из корзины перезапись сессии"""
    def delete(self, request, *args, **kwargs):

        return ServiceCart.delete_product_cart(request, *args, **kwargs)


class TotalSumProduct(APIView):
    """Получение общей суммы в корзине и проверка товара на наличие"""
    def get(self, request, *args, **kwargs):
        return ServiceCart.get_total_sum(request)
