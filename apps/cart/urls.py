from django.urls import path

from apps.cart.views import CreateCartView, DeleteProductCartView, ListCartView, TotalSumProduct

urlpatterns = [
    path('cart/add/<int:product_id>', CreateCartView.as_view(), name='add-cart'),
    path('cart/list', ListCartView.as_view(), name='list-cart'),
    path('cart/del/<int:product_id>', DeleteProductCartView.as_view(), name='del-cart'),
    path('cart/total_sum', TotalSumProduct.as_view(), name='total-sum-cart'),
]
