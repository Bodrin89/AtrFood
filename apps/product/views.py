from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404,)
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAdminUser

from apps.product.models import ProductModel
from apps.product.serializers import (AddProductCompareSerializer,
                                      AddProductFavoriteSerializer,
                                      CreateProductSerializer,
                                      ListProductSerializer,
                                      RetrieveProductSerializer,)
from config.settings import LOGGER


class CreateProductView(CreateAPIView):
    """Создание товара"""
    # permission_classes = [IsAdminUser]
    serializer_class = CreateProductSerializer


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
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category__name', 'existence', 'article', 'name', 'product_data__manufacturer']

    def get(self, request, *args, **kwargs):
        """Получение параметров пагинации из query_params)"""
        if page_size := self.request.query_params.get('page_size', None):
            self.pagination_class.page_size = int(page_size)
        return super().get(request, *args, **kwargs)


class ListProductSubcategoryView(ListAPIView):
    """Получение списка всех товаров по подкатегориям (получение похожих товаров)"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        subcategory_id = self.kwargs.get('subcategory_id')
        return ProductModel.objects.filter(category_id=category_id, subcategory_id=subcategory_id).all()


# class AddProductFavoriteView(CreateAPIView):
#     """Добавление/удаление товара в избранное"""
#     serializer_class = AddProductFavoriteSerializer
#
#     def perform_create(self, serializer):
#         product_id = self.kwargs.get('product_id')
#         product = get_object_or_404(ProductModel, id=product_id)
#         serializer.save(product=product)

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
