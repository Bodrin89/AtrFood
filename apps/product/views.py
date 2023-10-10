from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.product.models import ProductModel
from apps.product.serializers import CreateProductSerializer, RetrieveProductSerializer


class CreateProductView(CreateAPIView):
    """Создание товара"""
    # permission_classes = [IsAdminUser]
    serializer_class = CreateProductSerializer


class GetProductView(RetrieveAPIView):
    """Получение товара по id"""
    serializer_class = RetrieveProductSerializer
    queryset = ProductModel.objects.all()

#
# class ListProductView(ListAPIView):
#     """Получение списка всех товаров по подкатегориям"""
#     serializer_class = ListProductSerialiser


