from apps.product.models import FavoriteProductModel


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
