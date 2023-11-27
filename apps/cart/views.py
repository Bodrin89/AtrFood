from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from apps.cart.models import CartModel, CartItem
from apps.cart.serializers import CreateCartSerializer, ListCartSerializer
from apps.cart.services import ServiceCart


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
        ServiceCart.get_total_sum(cart_id)
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
