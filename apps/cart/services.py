from django.db.models import F, Q, QuerySet
from rest_framework import serializers, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from apps.company_user.models import CompanyUserModel
from apps.individual_user.models import IndividualUserModel
from apps.product.models import ProductModel
from apps.promotion.models import DiscountModel, LoyaltyModel
from apps.promotion.services import ServicePromotion
from apps.user.models import BaseUserModel
from config.settings import LOGGER


class ServiceCart:

    @staticmethod
    def _get_sum_price_product(price, quantity_product, discount_amounts):
        """Расчет суммы товаров в корзине с учетом всех скидок"""
        return (price - (price * sum(discount_amounts)) / 100) * quantity_product

    @staticmethod
    def _check_existence(product_id, quantity_product):
        """Проверка на наличие товара на складе и на наличие запрашиваемого количества"""
        try:
            ProductModel.objects.get(id=product_id, existence=True)
        except ProductModel.DoesNotExist:
            raise serializers.ValidationError({'error': _('Товара нет в наличии')})
        try:
            ProductModel.objects.get(id=product_id, quantity_stock__gte=quantity_product)
        except ProductModel.DoesNotExist:
            raise serializers.ValidationError({'error': _('Нужного количества нет на складе')})

    @staticmethod
    def _get_discount(product: ProductModel, quantity_product: int, limit_sum_product: float) -> QuerySet[DiscountModel]:
        """Фильтр акций по условиям"""
        discounts = product.products.all().filter(
            Q(is_active=True) &
            (Q(use_limit_person=True, count_person__lt=F('limit_person')) | ~Q(use_limit_person=True)) &
            (Q(use_limit_product=True, limit_product__gt=F('count_product') + quantity_product) | ~Q(
                use_limit_product=True)) &
            (Q(use_limit_sum_product=True, limit_sum_product__lt=limit_sum_product) | ~Q(use_limit_sum_product=True))
        )
        return discounts

    @staticmethod
    def _get_gifts_product(discount):
        """Проверка на наличие подарка в акции, получение списка подарков во всех акциях товара"""
        filtered_gifts = discount.filter(gift_id__isnull=False)

        gifts = []
        if filtered_gifts:
            for item in filtered_gifts.values():
                gift = ProductModel.objects.get(id=item['gift_id'])
                foto_url = gift.foto.url if gift.foto else None
                gifts.append({
                    'id': gift.id,
                    'name': gift.name,
                    'foto': foto_url,
                    'article': gift.article
                })
        return gifts


    @staticmethod
    def get_level_loyalty(user_id, discount_amounts):
        """Получение уровня лояльности"""
        try:
            user_type = BaseUserModel.objects.get(id=user_id).user_type
            loyalty = None

            if user_type == 'individual':
                try:
                    loyalty = IndividualUserModel.objects.get(baseusermodel_ptr_id=user_id).loyalty
                except IndividualUserModel.DoesNotExist:
                    pass
            elif user_type == 'company':
                try:
                    loyalty = CompanyUserModel.objects.get(baseusermodel_ptr_id=user_id).loyalty
                except CompanyUserModel.DoesNotExist:
                    pass

            if loyalty:
                try:
                    get_loyalty = LoyaltyModel.objects.get(id=loyalty.id)
                    loyalty_discount = get_loyalty.discount_percentage
                    discount_amounts.append(loyalty_discount)
                except LoyaltyModel.DoesNotExist:
                    pass

        except BaseUserModel.DoesNotExist:
            pass

    @staticmethod
    def add_cart(validated_data: dict) -> dict:
        """Сохранение товаров в корзину в сессии"""
        product_id = validated_data['product_id']
        session = validated_data['session']
        product_cart = session.get('product_cart', [])
        quantity_product = validated_data['quantity_product']
        product: ProductModel = validated_data['product']
        price = ProductModel.objects.get(id=product_id).price
        try:
            if quantity_product >= product.opt_quantity:
                price = product.opt_price
        except TypeError:
            pass

        limit_sum_product = price * quantity_product

        ServiceCart._check_existence(product_id, quantity_product)

        ServicePromotion.check_date_promotions()

        # discounts = ServiceCart._get_discount(product, quantity_product, limit_sum_product)
        # discount_amounts = [discount.discount_amount for discount in discounts]
        #
        # gifts = ServiceCart._get_gifts_product(discounts)
        #
        # if validated_data['user'].id and product.products.filter(use_limit_loyalty=True).exists():
        #     user_id = validated_data['user'].id
        #     ServiceCart.get_level_loyalty(user_id, discount_amounts)


        discounts = ServiceCart._get_discount(product, quantity_product, limit_sum_product)
        discount_amounts = [discount.discount_amount for discount in discounts]

        gifts = ServiceCart._get_gifts_product(discounts)

        user_id = validated_data['user'].id
        if user_id:
            if product.products.filter(use_limit_loyalty=True).exists() or not product.products.exists():
                ServiceCart.get_level_loyalty(user_id, discount_amounts)


        found = False
        for item in product_cart:
            if item.get('product_id') == product_id:
                item['quantity_product'] = quantity_product
                item['sum_products'] = ServiceCart._get_sum_price_product(price, quantity_product, discount_amounts)
                item['gifts'] = gifts
                found = True
                break

        if not found:
            product_cart.append({
                'product_id': product_id,
                'quantity_product': quantity_product,
                'sum_products': ServiceCart._get_sum_price_product(price, quantity_product, discount_amounts),
                'gifts': gifts
            })
        session['product_cart'] = product_cart
        session.modified = True
        for item in discounts:
            item.count_person += 1
            item.count_product += quantity_product
            item.save()
        return validated_data

    @staticmethod
    def get_list_product_cart(instance):
        """Получение всех товаров из корзины и их количества в заказе"""
        product_id = instance['product_id']
        quantity_product = instance['quantity_product']
        sum_products = instance['sum_products']
        gifts = instance['gifts']

        try:
            product = ProductModel.objects.get(id=product_id)
            product_data = {
                'product_id': product_id,
                'quantity_product': quantity_product,
                'sum_products': sum_products,
                'gifts': gifts,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                }
            }
        except ProductModel.DoesNotExist:
            product_data = {
                'product_id': product_id,
                'quantity_product': quantity_product,
                'product': None
            }
        return product_data

    @staticmethod
    def delete_product_cart(request, *args, **kwargs):
        """Удаление товара из корзины перезапись сессии"""
        product_cart = request.session.get('product_cart', [])
        product_id = kwargs.get('product_id')

        if not any(item.get('product_id') == product_id for item in product_cart):
            return Response({'message': _('Товар не найден в корзине')}, status=status.HTTP_404_NOT_FOUND)

        updated_cart = [item for item in product_cart if item.get('product_id') != product_id]

        request.session['product_cart'] = updated_cart
        request.session.modified = True
        return Response({'message': _('Товар удален из корзины')}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_total_sum(request):
        """Получение общей суммы в корзине и проверка товара на наличие"""
        product_cart = request.session.get('product_cart', [])
        total_sum = []
        not_existence = []
        for item in product_cart:
            product = ProductModel.objects.get(id=item.get('product_id'))
            if product.existence is True:
                total_sum.append(item.get('sum_products'))
            else:
                not_existence.append(product.id)
        return Response({'total_sum': sum(total_sum), _('Товары не в наличии'): not_existence})
