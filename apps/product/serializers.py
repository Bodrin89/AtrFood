
from rest_framework import serializers

from apps.product.models import ProductModel, CategoryProductModel, SubCategoryProductModel, DescriptionProductModel, \
    FavoriteProductModel
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
    category = CategorySerializer()
    subcategory = SubCategoryProductSerializer()
    product_data = DescriptionProductSerializer()

    class Meta:
        model = ProductModel
        fields = ('id', 'name', 'foto', 'price', 'discount', 'discount_price', 'product_data', 'quantity_stock',
                  'category', 'subcategory')
        read_only_fields = ('id', 'discount_price',)

    def create(self, validated_data):
        return ServiceProduct.create_product(validated_data)


class RetrieveProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'


class ListProductSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryProductSerializer()

    class Meta:
        model = ProductModel
        fields = '__all__'


class AddProductFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProductModel
        fields = '__all__'

    def create(self, validated_data):
        pass # TODO не реализовано




