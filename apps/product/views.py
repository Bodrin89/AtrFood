from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.product.models import ProductModel
from apps.product.serializers import CreateProductSerializer, RetrieveProductSerializer, ListProductSerializer
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
        return ProductModel.objects.filter(product_data_id=pk)


class ListProductView(ListAPIView):
    """Получение списка всех товаров по подкатегориям"""
    serializer_class = ListProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        subcategory_id = self.kwargs.get('subcategory_id')
        return ProductModel.objects.filter(category_id=category_id, subcategory_id=subcategory_id).all()


