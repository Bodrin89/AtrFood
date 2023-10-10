from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from apps.product.serializers import CreateProductSerializer


class CreateProductView(CreateAPIView):
    # permission_classes = [IsAdminUser]
    serializer_class = CreateProductSerializer

