
from rest_framework import serializers

from apps.product.models import ProductModel, CategoryProductModel, SubCategoryProductModel
from apps.product.services import ServiceProduct
from config.settings import LOGGER


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProductModel
        fields = ('name',)


class SubCategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryProductModel
        fields = ('name',)


class CreateProductSerializer(serializers.ModelSerializer):
    # quantity_select = serializers.IntegerField(required=False)
    category = CategorySerializer()
    subcategory = SubCategoryProductSerializer()

    class Meta:
        model = ProductModel
        fields = ('name', 'foto', 'price', 'discount', 'description', 'category', 'subcategory')

    def create(self, validated_data):
        return ServiceProduct.create_product(validated_data)


