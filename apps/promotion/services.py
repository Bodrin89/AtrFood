from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

from apps.company_user.models import CompanyUserModel
from apps.individual_user.models import IndividualUserModel
from apps.order.models import Order
from apps.promotion.models import DiscountModel, LoyaltyModel
from apps.user.models import BaseUserModel


class ServicePromotion:
    @staticmethod
    def check_date_promotions():
        """Проверка даты акций и перенос в архив если дата прошла"""
        promotions = DiscountModel.objects.all()
        for item in promotions:
            if item.date_end_discount < timezone.now().date():
                item.is_active = False
                item.save()

    @staticmethod
    def update_level_loyalty(data):
        """Функция обновления уровня лояльности пользователя"""
        sum_total_price = Order.objects.filter(user_id=data.user.id,
                                               status='completed').aggregate(Sum('total_price'))[
                              'total_price__sum'] or 0
        loyalty_levels = LoyaltyModel.objects.all()
        user: BaseUserModel = User.objects.get(id=data.user.id)

        loyalty = None

        if sum_total_price < loyalty_levels.get(id=1).sum_step:
            loyalty = None
        elif loyalty_levels.get(id=1).sum_step <= sum_total_price <= loyalty_levels.get(id=2).sum_step:
            loyalty = loyalty_levels.get(id=1)
        elif loyalty_levels.get(id=2).sum_step <= sum_total_price <= loyalty_levels.get(id=3).sum_step:
            loyalty = loyalty_levels.get(id=2)
        elif loyalty_levels.get(id=3).sum_step <= sum_total_price <= loyalty_levels.get(id=4).sum_step:
            loyalty = loyalty_levels.get(id=3)
        elif sum_total_price >= loyalty_levels.get(id=4).sum_step:
            loyalty = loyalty_levels.get(id=4)

        if user.user_type == 'individual':
            individual_user = IndividualUserModel.objects.get(baseusermodel_ptr_id=user.id)
            individual_user.loyalty = loyalty
            individual_user.save()
        elif user.user_type == 'company':
            company_user = CompanyUserModel.objects.get(baseusermodel_ptr_id=user.id)
            company_user.loyalty = loyalty
            company_user.save()
