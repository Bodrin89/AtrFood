from rest_framework import serializers

from apps.product.serializers import ListProductSerializer
from apps.promotion.models import DiscountModel


class ListDiscountSerializer(serializers.ModelSerializer):
    """Список всех акций"""
    product = ListProductSerializer(many=True)
    class Meta:
        model = DiscountModel
        fields = '__all__'
        # fields = ('name', 'product')


