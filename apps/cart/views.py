from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
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
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id, is_active=True)
        serializer.save(session=self.request.session, product_id=product_id, product=product)


class ListCartView(ListAPIView):
    """Получение всех товаров из корзины и их количества в заказе"""
    serializer_class = ListCartSerializer

    def get_queryset(self):
        product_cart = self.request.session.get('product_cart', [])
        return product_cart


class DeleteProductCartView(DestroyAPIView):
    """Удаление товара из корзины перезапись сессии"""
    def delete(self, request, *args, **kwargs):
        return ServiceCart.delete_product_cart(request, *args, **kwargs)


class TotalSumProduct(APIView):
    """Получение общей суммы в корзине и проверка товара на наличие"""
    def get(self, request, *args, **kwargs):
        return ServiceCart.get_total_sum(request)
