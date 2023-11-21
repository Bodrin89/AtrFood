from django.db.models import F, Q, QuerySet, Sum
from rest_framework import serializers, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from apps.cart.models import CartModel, CartItem
from apps.company_user.models import CompanyUserModel
from apps.individual_user.models import IndividualUserModel
from apps.product.models import ProductModel
from apps.promotion.models import DiscountModel, LoyaltyModel
from apps.promotion.services import ServicePromotion
from apps.user.models import BaseUserModel


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
    def _get_discount(product: ProductModel, quantity_product: int, limit_sum_product: float) -> QuerySet[
        DiscountModel]:
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
                gifts.append(gift)
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
        """Сохранение товаров в корзину"""
        cart_id = validated_data.get('cart_id')
        user_id = validated_data['user'].id
        list_product_id = []
        if not cart_id:
            cart = CartModel.objects.create()
            cart_id = cart.id
        try:
            product_cart = CartModel.objects.get(id=cart_id)
        except CartModel.DoesNotExist:
            raise serializers.ValidationError({"error": "Корзина не найдена"})
        for item_data in validated_data['product_item']:
            product_id = int(item_data['id'])
            list_product_id.append(product_id)
            quantity_product = int(item_data['quantity_product'])
            product = ProductModel.objects.get(id=product_id)
            price = ProductModel.objects.get(id=product_id).price
            try:
                if quantity_product >= product.opt_quantity:
                    price = product.opt_price
            except TypeError:
                pass

            limit_sum_product = price * quantity_product

            ServiceCart._check_existence(product_id, quantity_product)

            ServicePromotion.check_date_promotions()

            discounts = ServiceCart._get_discount(product, quantity_product, limit_sum_product)
            discount_amounts = [discount.discount_amount for discount in discounts]

            gifts = ServiceCart._get_gifts_product(discounts)

            if user_id:
                if product.products.filter(use_limit_loyalty=True).exists() or not product.products.exists():
                    ServiceCart.get_level_loyalty(user_id, discount_amounts)

            if product_cart:
                found = False
                for item in product_cart.cart_item.all():
                    if item.id == product_id:
                        item.quantity_product = quantity_product
                        item.sum_products = ServiceCart._get_sum_price_product(price, quantity_product,
                                                                               discount_amounts)
                        item.gifts = gifts[0] if len(gifts) > 0 else None
                        item.save()
                        found = True
                        break

                if not found:
                    cart_item = product_cart.cart_item.filter(product_id=product_id).first()
                    gifts = gifts[0] if len(gifts) > 0 else None
                    sum_products = ServiceCart._get_sum_price_product(price, quantity_product, discount_amounts)
                    if not cart_item:
                        CartItem.objects.create(cart=product_cart, product=product,
                                                quantity_product=quantity_product,
                                                sum_products=sum_products,
                                                gifts=gifts)
                    else:
                        cart_item.quantity_product = quantity_product
                        cart_item.sum_products = ServiceCart._get_sum_price_product(price, quantity_product,
                                                                                    discount_amounts)

                        cart_item.save()

        product_cart.cart_item.exclude(product_id__in=list_product_id).delete()

        total_sum = CartItem.objects.filter(cart_id=cart_id).aggregate(total_sum=Sum('sum_products'))
        sum_products_sum = total_sum.get('total_sum', 0)
        product_cart.total_price = sum_products_sum
        if user_id:
            product_cart.user = BaseUserModel.objects.get(id=user_id)
        product_cart.save()
        return product_cart

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
    def get_total_sum(card_id):
        """Перерасчет суммы товаров в корзине"""
        product_cart = CartModel.objects.get(id=card_id)
        total_sum = product_cart.cart_item.all().aggregate(total_sum=Sum('sum_products'))
        sum_products_sum = total_sum.get('total_sum', 0)
        product_cart.total_price = sum_products_sum
        product_cart.save()
        return True
