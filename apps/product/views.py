from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from apps.product.filters import ProductFilter
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404,)
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAdminUser

from apps.product.models import ProductModel, CatalogModel, CategoryProductModel
from apps.product.serializers import (AddProductCompareSerializer,
                                      AddProductFavoriteSerializer,
                                      ListProductSerializer,
                                      RetrieveProductSerializer, ListCatalogSerializer, CategorySerializer, )
from config.settings import LOGGER


# class CreateProductView(CreateAPIView):
#     """Создание товара"""
#     # permission_classes = [IsAdminUser]
#     serializer_class = CreateProductSerializer


class GetProductView(RetrieveAPIView):
    """Получение товара по id"""
    serializer_class = RetrieveProductSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return ProductModel.objects.filter(id=pk)


class ListProductView(ListAPIView):
    """Получение всех товаров с возможностью фильтрации"""
    serializer_class = ListProductSerializer
    queryset = ProductModel.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    # filterset_fields = [
    #     'subcategory__category__name',
    #     'existence',
    #     'article',
    #     'name',
    #     'product_data__manufacturer',
    #     'product_data__made_in'
    # ]

    def get(self, request, *args, **kwargs):
        """Получение параметров пагинации из query_params)"""
        if page_size := self.request.query_params.get('page_size', None):
            self.pagination_class.page_size = int(page_size)
        return super().get(request, *args, **kwargs)


class ListProductSubcategoryView(ListAPIView):
    """Получение списка всех товаров по подкатегориям (получение похожих товаров)"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs.get('subcategory_id')
        return ProductModel.objects.filter(subcategory_id=subcategory_id).all()


class ListProductCategoryView(ListAPIView):
    """Получение всех товаров в категории"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return ProductModel.objects.filter(subcategory__category_id=category_id).all()


class ListProductCatalogView(ListAPIView):
    """Получение всех товаров в каталоге"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        catalog_id = self.kwargs.get('catalog_id')
        return ProductModel.objects.filter(subcategory__category_id__catalog_id=catalog_id).all()


class ListCatalogView(ListAPIView):
    """Получение всех каталогов"""
    queryset = CatalogModel.objects.all()
    serializer_class = ListCatalogSerializer


class ListCategorySubcategoryView(ListAPIView):
    """Получение всех категорий каталога с подкатегориями категории"""
    # queryset = CategoryProductModel.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        catalog_id = self.kwargs.get('catalog_id')
        return CategoryProductModel.objects.filter(catalog_id=catalog_id).all()


class AddProductFavoriteView(CreateAPIView):
    """Добавление/удаление товара в избранное"""
    serializer_class = AddProductFavoriteSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        serializer.save(session=self.request.session, product_id=product_id, product=product)


class AddProductCompareView(CreateAPIView):
    """Добавление/удаление товара для сравнения"""
    serializer_class = AddProductCompareSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        serializer.save(session=self.request.session, product_id=product_id, product=product)


class ListFavoriteProductView(ListAPIView):
    """Список избранных товаров пользователя"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        favorite_product_ids = self.request.session.get('favorite', [])
        return ProductModel.objects.filter(id__in=favorite_product_ids)


class ListCompareProductView(ListAPIView):
    """Список товаров для сравнения пользователя"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        compare_product_ids = self.request.session.get('compare', [])
        if len(compare_product_ids) <= 1:
            raise ValueError('Необходимо два товара для сравнения')
        return ProductModel.objects.filter(id__in=compare_product_ids)
