from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, \
    get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

from apps.product.models import ProductModel
from apps.product.serializers import CreateProductSerializer, RetrieveProductSerializer, ListProductSerializer, \
    AddProductFavoriteSerializer, AddProductCompareSerializer
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
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category__name', 'existence', 'article', 'name', 'product_data__manufacturer']


class ListProductSubcategoryView(ListAPIView):
    """Получение списка всех товаров по подкатегориям (получение похожих товаров)"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        subcategory_id = self.kwargs.get('subcategory_id')
        return ProductModel.objects.filter(category_id=category_id, subcategory_id=subcategory_id).all()


class AddProductFavoriteView(CreateAPIView):
    """Добавление/удаление товара в избранное"""
    serializer_class = AddProductFavoriteSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        serializer.save(product=product)


class AddProductCompareView(CreateAPIView):
    """Добавление/удаление товара для сравнения"""
    serializer_class = AddProductCompareSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        serializer.save(product=product)

#
# class ListFavoriteProductView(ListAPIView):
#
#     serializer_class = ListProductSerializer
#
#     def get_queryset(self):
#         return






