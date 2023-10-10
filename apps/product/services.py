import random

from django.utils.crypto import get_random_string

from apps.product.models import CategoryProductModel, SubCategoryProductModel, ProductModel
from config.settings import LOGGER
from django.db import transaction


class ServiceProduct:

    @staticmethod
    def create_product(validated_data: dict) -> ProductModel:
        """Создание товара"""
        category_product_data = validated_data.pop('category', None)
        subcategory_product_data = validated_data.pop('subcategory', None)
        category, _ = CategoryProductModel.objects.get_or_create(**category_product_data)
        subcategory, _ = SubCategoryProductModel.objects.get_or_create(category=category, **subcategory_product_data)
        existence = True
        product = ProductModel.objects.create(category=category, existence=existence, subcategory=subcategory,
                                              **validated_data)
        return product

