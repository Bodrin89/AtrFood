from django.urls import path

from apps.product.views import CreateProductView

urlpatterns = [
    path('create_product', CreateProductView.as_view(), name='create-product'),
]
