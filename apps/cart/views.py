from rest_framework import serializers
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from apps.cart.models import CartModel, CartItem
from apps.cart.serializers import CreateCartSerializer, ListCartSerializer
from apps.cart.services import ServiceCart
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
        user = self.request.user
        cart_id = self.kwargs.get('pk')
        try:
            ServiceCart.get_total_sum(cart_id)
            if user.id:
                ServiceCart.check_owner_cart(cart_id, user_id=user.id)
                product_cart = CartModel.objects.filter(id=cart_id, user_id=user.id)
                return product_cart
            else:
                product_cart = CartModel.objects.filter(id=cart_id)
                return product_cart
        except CartModel.DoesNotExist:
            raise serializers.ValidationError({"error": "Корзина не найдена"})


class DeleteProductCartView(DestroyAPIView):
    """Удаление товара из корзины"""
    def delete(self, request, *args, **kwargs):
        cart_id = self.request.data.get('cart_id')
        product_id = self.request.data.get('product_id')
        del_obj = CartItem.objects.filter(product_id=product_id, cart_id=cart_id)
        del_obj.delete()
        ServiceCart.get_total_sum(cart_id)
        return Response('Объект удален')
