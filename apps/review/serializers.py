
from rest_framework import serializers

from apps.product.models import ProductModel
from apps.review.models import ReviewProductModel
from apps.review.services import ServiceReview
from config.settings import LOGGER


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReviewProductModel
        fields = ('id', 'count_stars', 'review_text', 'foto', 'user')
        read_only_files = ('id',)

    def create(self, validated_data):
        return ServiceReview.create_review(validated_data)

    # def validate_product(self, value: ProductModel) -> ProductModel:
    #     # TODO Реалтзовать проверку купил ли пользователь этот товар!!!!
    #     return value
