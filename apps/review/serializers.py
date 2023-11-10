from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from config.settings import LOGGER
from apps.review.models import ReviewProductModel, ReviewImage

User = get_user_model()


class UserMailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра почты пользователя"""

    class Meta:
        model = User
        fields = ('email',)
        read_only_files = ('id',)


class ReviewImageSerializer(serializers.ModelSerializer):
    """Сериализатор для создания фотографий к отзыву"""
    class Meta:
        model = ReviewImage
        fields = ('image',)


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Для создания и просмотра отзывов"""
    user = UserMailSerializer(read_only=True)
    images = ReviewImageSerializer(many=True, required=False, allow_empty=True)

    class Meta:
        model = ReviewProductModel
        fields = ('id', 'count_stars', 'review_text', 'user', 'product', 'images', 'date_created')
        read_only_files = ('id',)

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        request = self.context.get('request')
        user = request.user if request and hasattr(request, 'user') else None
        if user and user.is_authenticated:
            validated_data['user'] = user
        else:
            raise ValidationError({'error': _('Только авторизованный пользователь может оставить отзыв')})
        review = ReviewProductModel.objects.create(**validated_data)
        for image_data in images_data:
            ReviewImage.objects.create(review=review, **image_data)
        return review

    # def create(self, validated_data):
    #     return ServiceReview.create_review(validated_data)
