from django.urls import path

from apps.product.views import (AddProductCompareView,
                                AddProductFavoriteView,
                                GetProductView,
                                ListCompareProductView,
                                ListFavoriteProductView,
                                ListProductSubcategoryView,
                                ListProductView, ListProductCategoryView, ListProductCatalogView, ListCatalogView,
                                ListCategorySubcategoryView, )

urlpatterns = [
    # path('products/create', CreateProductView.as_view(), name='create-product'),
    path('products', ListProductView.as_view(), name='list-product'),
    path('products/subcategories/<int:subcategory_id>', ListProductSubcategoryView.as_view(),
         name='subcategory-products'),
    path('products/category/<int:category_id>', ListProductCategoryView.as_view(), name='category-products'),
    path('products/catalog/<int:catalog_id>', ListProductCatalogView.as_view(), name='catalog-products'),
    path('products/<int:pk>/retrieve', GetProductView.as_view(), name='retrieve-product'),
    path('products/<int:product_id>/favorite', AddProductFavoriteView.as_view(), name='add-favorite-product'),
    path('products/favorite', ListFavoriteProductView.as_view(), name='list-favorite-product'),
    path('products/<int:product_id>/compare', AddProductCompareView.as_view(), name='add-compare-product'),
    path('products/compare', ListCompareProductView.as_view(), name='add-compare-product'),
    path('products/catalogs', ListCatalogView.as_view(), name='list-catalog'),
    path('products/catalog/<int:catalog_id>/category', ListCategorySubcategoryView.as_view(),
         name='list-catalog-category-subcategory'),
]
