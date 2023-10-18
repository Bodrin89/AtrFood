from django.urls import path

from apps.product.views import (AddProductCompareView,
                                AddProductFavoriteView,
                                CreateProductView,
                                GetProductView,
                                ListCompareProductView,
                                ListFavoriteProductView,
                                ListProductSubcategoryView,
                                ListProductView,)

urlpatterns = [
    path('products/create', CreateProductView.as_view(), name='create-product'),
    path('products', ListProductView.as_view(), name='list-product'),
    path('categories/<int:category_id>/subcategories/<int:subcategory_id>/products/',
         ListProductSubcategoryView.as_view(), name='similar-product'),
    path('products/<int:pk>/retrieve', GetProductView.as_view(), name='retrieve-product'),
    path('products/<int:product_id>/favorite', AddProductFavoriteView.as_view(), name='add-favorite-product'),
    path('products/favorite', ListFavoriteProductView.as_view(), name='list-favorite-product'),
    path('products/<int:product_id>/compare', AddProductCompareView.as_view(), name='add-compare-product'),
    path('products/compare', ListCompareProductView.as_view(), name='add-compare-product'),
]
