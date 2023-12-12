from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from apps.order.models import Order
from apps.order.serializers import CreateOrderSerializer, GetOrderSerializer, GetAllOrderSerializer


class CreateOrderViewSet(ModelViewSet):
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class
        return GetOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(request=self.request)




#TODO View for 1C

class GetAllOrderView(ListAPIView):
    serializer_class = GetAllOrderSerializer
    queryset = Order.objects.all()

