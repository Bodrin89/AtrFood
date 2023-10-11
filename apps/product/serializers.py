
from rest_framework import serializers

from apps.product.models import ProductModel, CategoryProductModel, SubCategoryProductModel, DescriptionProductModel, \
    FavoriteProductModel, CompareProductModel
from apps.product.services import ServiceProduct
from config.settings import LOGGER


class CategorySerializer(serializers.ModelSerializer):
    """Категория"""
    class Meta:
        model = CategoryProductModel
        fields = ('name',)


class SubCategoryProductSerializer(serializers.ModelSerializer):
    """Подкатегория"""
    class Meta:
        model = SubCategoryProductModel
        fields = ('name',)


class DescriptionProductSerializer(serializers.ModelSerializer):
    """Описание товара"""
    class Meta:
        model = DescriptionProductModel
        fields = ('manufacturer', 'made_in', 'description', 'package')


class CreateProductSerializer(serializers.ModelSerializer):
    """Создание товара"""
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
    """Получение товара по id"""
    class Meta:
        model = ProductModel
        fields = '__all__'


class ListProductSerializer(serializers.ModelSerializer):
    """Получение всех товаров"""

    class Meta:
        model = ProductModel
        fields = '__all__'


class AddProductFavoriteSerializer(serializers.ModelSerializer):
    """Добавление/удаление товара в избранное"""
    class Meta:
        model = FavoriteProductModel
        fields = ('id',)

    def create(self, validated_data):
        return ServiceProduct.add_delete_product_favorite(validated_data)


class AddProductCompareSerializer(serializers.ModelSerializer):
    """Добавление/удаление товара для сравнения"""
    class Meta:
        model = CompareProductModel
        fields = ('id',)

    def create(self, validated_data):
        return ServiceProduct.add_delete_product_compare(validated_data)



# class AddProductCompareSerializer(serializers.ModelSerializer):
#     """Добавление/удаление товара для сравнения"""
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = CompareProductModel
#         fields = ('id', 'user')
#
#     def create(self, validated_data):
#         return ServiceProduct.add_delete_product_compare(validated_data)





