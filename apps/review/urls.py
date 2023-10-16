from django.urls import path

from apps.review.views import (
    # ReviewCreateView,
    ReviewProductViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', ReviewProductViewSet, basename='review')

urlpatterns = [
    # path('products/<int:product_id>/reviews', ReviewCreateView.as_view(), name='add-review'),
] + router.urls
