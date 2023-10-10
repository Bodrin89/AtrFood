
from apps.product.models import CategoryProductModel, SubCategoryProductModel, ProductModel
from config.settings import LOGGER
from django.db import transaction


class ServiceProduct:

    @staticmethod
    def _calculation_discount(price: int, discount: int) -> float:
        """Расчет цены с учетом скидки"""
        result_price = price - (price * discount) / 100
        return result_price

    @staticmethod
    def create_product(validated_data: dict) -> ProductModel:
        """Создание товара"""
        with transaction.atomic():
            category_product_data = validated_data.pop('category', None)
            subcategory_product_data = validated_data.pop('subcategory', None)
            category, _ = CategoryProductModel.objects.get_or_create(**category_product_data)
            subcategory, _ = SubCategoryProductModel.objects.get_or_create(category=category, **subcategory_product_data)
            existence = True
            discount = validated_data.pop('discount', None)
            price = validated_data.get('price', None)
            if discount:
                discount_price = ServiceProduct._calculation_discount(price, discount)
                product = ProductModel.objects.create(category=category, discount_price=discount_price, existence=existence,
                                                      subcategory=subcategory, **validated_data)
            else:
                product = ProductModel.objects.create(category=category, discount_price=price, existence=existence,
                                                      subcategory=subcategory, **validated_data)
        return product
