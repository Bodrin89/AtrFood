from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

from apps.company_user.models import CompanyUserModel
from apps.individual_user.models import IndividualUserModel
from apps.promotion.models import DiscountModel, LoyaltyModel
from apps.user.models import BaseUserModel
from config.settings import LOGGER


class ServicePromotion:
    @staticmethod
    def check_date_promotions():
        """Проверка даты акций и перенос в архив если дата прошла"""
        promotions = DiscountModel.objects.all()
        for item in promotions:
            if item.date_end_discount < timezone.now().date():
                item.is_active = False
                item.save()
