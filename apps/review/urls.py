from django.urls import path

from apps.review.views import ReviewCreateView

urlpatterns = [
    path('products/<int:product_id>/reviews', ReviewCreateView.as_view(), name='add-review'),
]
