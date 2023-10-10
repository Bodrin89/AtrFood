from django.urls import path

from apps.product.views import CreateProductView, GetProductView, ListProductSubcategoryView, ListProductView

urlpatterns = [
    path('create_products', CreateProductView.as_view(), name='create-product'),
    path('products', ListProductView.as_view(), name='list-product'),
    path('categories/<int:category_id>/subcategories/<int:subcategory_id>/products/',
         ListProductSubcategoryView.as_view(), name='similar-product'),
    path('retrieve_product/<int:pk>', GetProductView.as_view(), name='retrieve-product'),
]
