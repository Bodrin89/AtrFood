from django.utils import timezone

from apps.promotion.models import DiscountModel


class ServicePromotion:
    @staticmethod
    def check_date_promotions():
        """Проверка даты акций и перенос в архив если дата прошла"""
        promotions = DiscountModel.objects.all()
        for item in promotions:
            if item.date_end_discount < timezone.now().date():
                item.is_active = False
                item.save()
