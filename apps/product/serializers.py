from rest_framework import serializers
from apps.product.models import (CatalogModel,
                                 CategoryProductModel,
                                 CompareProductModel,
                                 DescriptionProductModel,
                                 FavoriteProductModel,
                                 ProductModel,
                                 SubCategoryProductModel,
                                 ProductImage,)
from apps.product.services import ServiceProduct
from apps.library.serializers import ManufacturingCompanySerializer, CountrySerializer
from config.settings import LOGGER


class SubCategoryProductSerializer(serializers.ModelSerializer):
    """Подкатегория"""
    class Meta:
        model = SubCategoryProductModel
        fields = ('name', 'id')


class CategorySerializer(serializers.ModelSerializer):
    """Категория"""
    subcategories = SubCategoryProductSerializer(many=True)

    class Meta:
        model = CategoryProductModel
        fields = ('name', 'subcategories', 'id')


class CatalogSerializer(serializers.ModelSerializer):
    """Каталог"""

    class Meta:
        model = CatalogModel
        fields = ('name', 'id')


class DescriptionProductSerializer(serializers.ModelSerializer):
    """Описание товара"""
    manufacturer = ManufacturingCompanySerializer()
    made_in = CountrySerializer()

    class Meta:
        model = DescriptionProductModel
        fields = ('manufacturer', 'made_in', 'description')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ListProductSerializer(serializers.ModelSerializer):
    """Получение всех товаров"""

    product_data = DescriptionProductSerializer()
    subcategory = SubCategoryProductSerializer()
    images = ProductImageSerializer(source='images.all', many=True)

    class Meta:
        model = ProductModel
        fields = '__all__'


# class CreateProductSerializer(serializers.ModelSerializer):
#     """Создание товара"""
#     # catalog = CatalogSerializer()
#     # category = CategorySerializer()
#     subcategory = SubCategoryProductSerializer()
#     product_data = DescriptionProductSerializer()
#
#     class Meta:
#         model = ProductModel
#         fields = ('id', 'name', 'foto', 'price', 'discount_price', 'product_data', 'quantity_stock', 'subcategory')
#         read_only_fields = ('id', 'discount_price',)
#
#     def create(self, validated_data):
#         return ServiceProduct.create_product(validated_data)

class ListCatalogSerializer(serializers.ModelSerializer):
    """Получение всех каталогов с вложенными категориями/подкатегориями"""

    catalogs = CategorySerializer(many=True)

    class Meta:
        model = CatalogModel
        fields = ('name', 'catalogs', 'id')


class RetrieveProductSerializer(serializers.ModelSerializer):
    """Получение товара по id"""

    product_data = DescriptionProductSerializer()
    subcategory = SubCategoryProductSerializer()
    images = ProductImageSerializer(source='images.all', many=True)

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


class ProductInfoSerializer(serializers.ModelSerializer):
    """Получение всех товаров в заказ"""

    class Meta:
        model = ProductModel
        fields = [
            'name',
            'price',
            'article',
            'discount_price',
        ]


class GiftInfoSerializer(serializers.ModelSerializer):
    """Информация по подарку из акции"""
    images = ProductImageSerializer(source='images.all', many=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'images', 'article', ]

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
