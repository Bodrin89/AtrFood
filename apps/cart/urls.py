from django.urls import path

from apps.cart.views import CreateCartView, DeleteProductCartView, ListCartView

urlpatterns = [
    path('add', CreateCartView.as_view(), name='add-cart'),
    path('list/<int:pk>', ListCartView.as_view(), name='list-cart'),
    path('delete', DeleteProductCartView.as_view(), name='del-cart'),
    # path('total_sum', TotalSumProduct.as_view(), name='total-sum-cart'),
]
