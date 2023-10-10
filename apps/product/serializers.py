
from rest_framework import serializers

from apps.product.models import ProductModel, CategoryProductModel, SubCategoryProductModel, DescriptionProductModel
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


class DescriptionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionProductModel
        fields = ('manufacturer', 'made_in', 'description', 'package')


class CreateProductSerializer(serializers.ModelSerializer):
    # quantity_select = serializers.IntegerField(required=False)
    category = CategorySerializer()
    subcategory = SubCategoryProductSerializer()
    product_data = DescriptionProductSerializer()

    class Meta:
        model = ProductModel
        fields = ('name', 'foto', 'price', 'discount', 'discount_price', 'product_data', 'quantity_stock',
                  'category', 'subcategory')
        read_only_fields = ('discount_price',)

    def create(self, validated_data):
        return ServiceProduct.create_product(validated_data)


class RetrieveProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'



