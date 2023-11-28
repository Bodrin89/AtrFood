from rest_framework import serializers
from apps.product.models import (CatalogModel,
                                 CategoryProductModel,
                                 CompareProductModel,
                                 DescriptionProductModel,
                                 FavoriteProductModel,
                                 ProductModel,
                                 SubCategoryProductModel,
                                 ProductImage,
                                 )
from apps.product.services import ServiceProduct
from apps.library.serializers import ManufacturingCompanySerializer, CountrySerializer, PackageTypeSerializer
from apps.review.models import ReviewProductModel
from apps.review.serializers import ReviewImageSerializer
from config.settings import LOGGER


class SubCategoryProductSerializer(serializers.ModelSerializer):
    """Подкатегория"""
    class Meta:
        model = SubCategoryProductModel
        fields = ('name', 'image', 'id')


class CategorySerializer(serializers.ModelSerializer):
    """Категория"""
    subcategories = SubCategoryProductSerializer(many=True)

    class Meta:
        model = CategoryProductModel
        fields = ('name', 'image', 'subcategories', 'id')


class CategoryListSerializer(serializers.ModelSerializer):
    """Список всех категорий"""

    class Meta:
        model = CategoryProductModel
        fields = ('name', 'image', 'id')


class CatalogSerializer(serializers.ModelSerializer):
    """Каталог"""

    class Meta:
        model = CatalogModel
        fields = ('name', 'id')


class DescriptionProductSerializer(serializers.ModelSerializer):
    """Описание товара"""
    manufacturer = ManufacturingCompanySerializer()
    made_in = CountrySerializer()
    package = PackageTypeSerializer()

    class Meta:
        model = DescriptionProductModel
        fields = ('manufacturer', 'made_in', 'description', 'package')


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


class PopularCategoriesSerializer(serializers.ModelSerializer):
    """Получение популярных категорий"""

    class Meta:
        model = CategoryProductModel
        fields = ['id', 'name', 'image',]

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

    categories = CategorySerializer(many=True)

    class Meta:
        model = CatalogModel
        fields = ('name', 'categories', 'id')


class RetrieveProductSerializer(serializers.ModelSerializer):
    """Получение товара по id"""

    product_data = DescriptionProductSerializer()
    subcategory = SubCategoryProductSerializer()
    images = ProductImageSerializer(source='images.all', many=True)

    class Meta:
        model = ProductModel
        fields = '__all__'


class AddProductFavoriteSerializer(serializers.ModelSerializer):
    """Добавление товара в избранное"""
    class Meta:
        model = FavoriteProductModel
        fields = ('id',)

    def create(self, validated_data):
        favorite_products = ServiceProduct.add_delete_product_favorite(validated_data)

        return favorite_products


class AddProductCompareSerializer(serializers.ModelSerializer):
    """Добавление/удаление товара для сравнения"""
    class Meta:
        model = CompareProductModel
        fields = ('id',)

    def create(self, validated_data):
        return ServiceProduct.add_delete_product_compare(validated_data)


class ProductInfoSerializer(serializers.ModelSerializer):
    """Получение всех товаров в заказ"""
    images = ProductImageSerializer(source='images.all', many=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'article', 'discount_price', 'images', 'opt_price', 'existence', 'rating']


class FavoriteProductInfoSerializer(serializers.ModelSerializer):
    """Получение всех товаров в заказ"""
    images = ProductImageSerializer(source='images.all', many=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'article', 'discount_price', 'opt_price', 'existence', 'images']


class ListFavoriteProductSerializer(serializers.ModelSerializer):
    """Получение избранных товаров"""
    product = FavoriteProductInfoSerializer()

    class Meta:
        model = ProductModel
        fields = ('product',)


class GiftInfoSerializer(serializers.ModelSerializer):
    """Информация по подарку из акции"""
    images = ProductImageSerializer(source='images.all', many=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'images', 'article', ]


class GetProductListSerializer(serializers.Serializer):
    """Получение списка ключей продуктов"""
    product_keys = serializers.ListField(child=serializers.IntegerField())


class ProductReviewInfoSerializer(serializers.ModelSerializer):
    """Вывод товара с отзывом пользователя"""
    images = ProductImageSerializer(source='images.all', many=True)
    review_text = serializers.SerializerMethodField()
    id_review = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ('id', 'images', 'name', 'rating', 'review_text', 'id_review')

    def get_id_review(self, obj: ProductModel):
        user = self.context['request'].user
        review = obj.review_product.filter(user=user).first()
        return review.id if review else None

    def get_review_text(self, obj: ProductModel):
        user = self.context['request'].user
        review = obj.review_product.filter(user=user).first()
        return review.review_text if review else None
