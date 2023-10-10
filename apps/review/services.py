from apps.review.models import ReviewProductModel


class ServiceReview:

    @staticmethod
    def create_review(validated_data: dict) -> ReviewProductModel:
        """Добавление комментария к товару"""
        review = ReviewProductModel.objects.create(**validated_data)
        return review
