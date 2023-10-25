from django.db import transaction

from apps.product.models import (CategoryProductModel,
                                 CompareProductModel,
                                 DescriptionProductModel,
                                 FavoriteProductModel,
                                 ProductModel,
                                 SubCategoryProductModel,)
from config.settings import LOGGER


class ServiceProduct:

    @staticmethod
    def _calculation_discount(price: int, discount: int) -> float:
        """Расчет цены с учетом скидки"""
        result_price = price - (price * discount) / 100
        return result_price

    @staticmethod
    def _calculation_existence(quantity_stock: int, quantity_select: int = 0) -> bool:
        """Расчет наличия товара на складе (есть/нет)"""
        if quantity_stock - quantity_select > 0:
            return True
        return False

    # @staticmethod
    # def create_product(validated_data: dict) -> ProductModel:
    #     """Создание товара"""
    #     with transaction.atomic():
    #         category_product_data = validated_data.pop('category', None)
    #         subcategory_product_data = validated_data.pop('subcategory', None)
    #         category, _ = CategoryProductModel.objects.get_or_create(**category_product_data)
    #         subcategory, _ = SubCategoryProductModel.objects.get_or_create(category=category,
    #                                                                        **subcategory_product_data)
    #         existence = ServiceProduct._calculation_existence(validated_data['quantity_stock'])
    #         product_data = validated_data.pop('product_data', None)
    #         product_data, _ = DescriptionProductModel.objects.get_or_create(**product_data)
    #         discount = validated_data.pop('discount', None)
    #         price = validated_data.get('price', None)
    #         if discount:
    #             discount_price = ServiceProduct._calculation_discount(price, discount)
    #             product = ProductModel.objects.create(category=category, product_data=product_data,
    #                                                   discount_price=discount_price, discount=discount,
    #                                                   existence=existence, subcategory=subcategory, **validated_data)
    #         else:
    #             product = ProductModel.objects.create(category=category, product_data=product_data,
    #                                                   discount_price=price, existence=existence,
    #                                                   subcategory=subcategory, **validated_data)
    #     return product

    # @staticmethod
    # def create_product(validated_data: dict) -> ProductModel:
    #     """Создание товара"""
    #     with transaction.atomic():
    #         subcategory_product_data = validated_data.pop('subcategory', None)
    #         subcategory, _ = SubCategoryProductModel.objects.get_or_create(**subcategory_product_data)
    #         existence = ServiceProduct._calculation_existence(validated_data['quantity_stock'])
    #         product_data = validated_data.pop('product_data', None)
    #         product_data, _ = DescriptionProductModel.objects.get_or_create(**product_data)
    #         discount = validated_data.pop('discount', None)
    #         price = validated_data.get('price', None)
    #         if discount:
    #             discount_price = ServiceProduct._calculation_discount(price, discount)
    #             product = ProductModel.objects.create(product_data=product_data,
    #                                                   discount_price=discount_price, discount=discount,
    #                                                   existence=existence, subcategory=subcategory, **validated_data)
    #         else:
    #             product = ProductModel.objects.create(product_data=product_data,
    #                                                   discount_price=price, existence=existence,
    #                                                   subcategory=subcategory, **validated_data)
    #     return product

    @staticmethod
    def add_delete_product_favorite(validated_data: dict) -> FavoriteProductModel:
        """Добавление/удаление товара в избранное"""

        favorite = validated_data['session'].get('favorite', [])
        if validated_data['product_id'] not in favorite:
            favorite.append(validated_data['product_id'])
        else:
            favorite.remove(validated_data['product_id'])
        validated_data['session']['favorite'] = favorite
        validated_data['session'].modified = True
        return favorite

    @staticmethod
    def add_delete_product_compare(validated_data):
        """Добавление/удаление товара для сравнения"""

        compare = validated_data['session'].get('compare', [])
        if validated_data['product_id'] not in compare:
            compare.append(validated_data['product_id'])
        else:
            compare.remove(validated_data['product_id'])
        validated_data['session']['compare'] = compare
        validated_data['session'].modified = True
        return validated_data

        # @staticmethod
    # def add_delete_product_compare(validated_data: dict) -> CompareProductModel:
    #     compare_product, create = CompareProductModel.objects.get_or_create(**validated_data)
    #     if create:
    #         return compare_product
    #     return compare_product.delete()

    @staticmethod
    def add_viewed_products(product_id, request):
        """Добавление просмотренные товары в сессию"""

        viewed_products = request.session.get('viewed_products', [])
        if product_id not in viewed_products:
            viewed_products.insert(0, product_id)
        request.session['viewed_products'] = viewed_products[:20]
        request.session.modified = True
        return request
