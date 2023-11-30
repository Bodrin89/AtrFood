from django.db import transaction
from rest_framework import serializers

from apps.library.models import ManufacturingCompany, CountryManufacturer, PackageType
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
        fields = ['id', 'name', 'image', ]


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
    count_star = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ('id', 'images', 'name', 'review_text', 'id_review', 'count_star')

    def get_count_star(self, obj: ProductModel):
        user = self.context['request'].user
        review = obj.review_product.filter(user=user).first()
        return review.count_stars if review else None

    def get_id_review(self, obj: ProductModel):
        user = self.context['request'].user
        review = obj.review_product.filter(user=user).first()
        return review.id if review else None

    def get_review_text(self, obj: ProductModel):
        user = self.context['request'].user
        review = obj.review_product.filter(user=user).first()
        return review.review_text if review else None






class CreateCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogModel
        fields = '__all__'

    def create(self, validated_data):
        return CatalogModel.objects.create(**validated_data)


class CreateCategorySerializer(serializers.ModelSerializer):
    catalog = CatalogSerializer()

    class Meta:
        model = CategoryProductModel
        fields = ('name', 'image', 'popularity', 'catalog')

    def create(self, validated_data):
        catalog_name = validated_data.pop('catalog').get('name')
        catalog, _ = CatalogModel.objects.get_or_create(name=catalog_name)
        return CategoryProductModel.objects.create(**validated_data, catalog=catalog)


class CreateSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategoryProductModel
        fields = ('name', 'image', 'category')

    def create(self, validated_data):
        return SubCategoryProductModel.objects.create(**validated_data)


class CreateProductSerializer(serializers.ModelSerializer):
    images = serializers.ImageField()
    product_data = DescriptionProductSerializer()

    class Meta:
        model = ProductModel
        fields = '__all__'

    def create(self, validated_data):
        images = validated_data.pop('images')
        product_data = validated_data.pop('product_data')

        manufacturingcompany, _ = ManufacturingCompany.objects.get_or_create(
            name=product_data.get('manufacturer').get('name'), logo=product_data.get('manufacturer').get('logo'))
        made_in, _ = CountryManufacturer.objects.get_or_create(name=product_data.get('made_in').get('name'))
        package, _ = PackageType.objects.get_or_create(name=product_data.get('package').get('name'))

        product, _ = ProductModel.objects.get_or_create(**validated_data)

        ProductImage.objects.get_or_create(image=images, product=product)

        DescriptionProductModel.objects.create(
            manufacturer=manufacturingcompany,
            made_in=made_in,
            description=product_data.get('description'),
            package=package,
            product=product
        )
        return product
