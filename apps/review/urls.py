from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.review.views import ReviewProductViewSet  # ReviewCreateView,

router = DefaultRouter()

router.register(r'', ReviewProductViewSet, basename='review')

urlpatterns = [
    # path('products/<int:product_id>/reviews', ReviewCreateView.as_view(), name='add-review'),
] + router.urls
