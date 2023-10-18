from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.product.models import ProductModel
from apps.review.models import ReviewProductModel
from apps.review.services import ServiceReview
from config.settings import LOGGER

User = get_user_model()


class UserMailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра почты пользователя"""

    class Meta:
        model = User
        fields = ('email',)
        read_only_files = ('id',)


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Для создания и просмотра отзывов"""
    user = UserMailSerializer(read_only=True)

    class Meta:
        model = ReviewProductModel
        fields = ('id', 'count_stars', 'review_text', 'foto', 'user', 'product',)
        read_only_files = ('id',)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request and hasattr(request, 'user') else None
        if user and user.is_authenticated:
            validated_data['user'] = user
        else:
            raise ValidationError({'error': 'Только авторизованный пользователь может оставить отзыв'})
        return super().create(validated_data)

    # def create(self, validated_data):
    #     return ServiceReview.create_review(validated_data)
