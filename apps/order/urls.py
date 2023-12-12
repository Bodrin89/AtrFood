from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.order.views import CreateOrderViewSet, GetAllOrderView

router = DefaultRouter()

router.register(r'', CreateOrderViewSet, basename='order')


urlpatterns = [
    path('get_all_order', GetAllOrderView.as_view(), name='get-all-order')
] + router.urls
