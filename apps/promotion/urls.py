from django.urls import path

from apps.promotion.views import ListDiscountIsShowView, ListDiscountView

urlpatterns = [
    path('discounts', ListDiscountView.as_view(), name='list-discounts'),
    path('discounts/is_show', ListDiscountIsShowView.as_view(), name='list-discounts-is_show'),
]
