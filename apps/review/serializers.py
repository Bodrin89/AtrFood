
from rest_framework import serializers

from apps.product.models import ProductModel
from apps.review.models import ReviewProductView
from config.settings import LOGGER


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReviewProductView
        fields = ('id', 'count_stars', 'review_text', 'product', 'foto', 'user')
        read_only_files = ('id',)

    def validate_product(self, value: ProductModel) -> ProductModel:
        """Реалтзовать проверке купил ли пользователь этот товар!!!!"""
        return value
