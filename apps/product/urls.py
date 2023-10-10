from django.urls import path

from apps.product.views import CreateProductView, GetProductView

urlpatterns = [
    path('create_product', CreateProductView.as_view(), name='create-product'),
    path('retrieve_product/<int:pk>', GetProductView.as_view(), name='retrieve-product'),
]
