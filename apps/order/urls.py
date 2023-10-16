from rest_framework.routers import DefaultRouter
from apps.order.views import CreateOrderViewSet

router = DefaultRouter()

router.register(r'order', CreateOrderViewSet, basename='order')


urlpatterns = [
] + router.urls