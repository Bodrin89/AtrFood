from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.promotion.models import DiscountModel, LoyaltyModel


@admin.register(DiscountModel)
class DiscountAdmin(admin.ModelAdmin):
    pass

@admin.register(LoyaltyModel)
class LoyaltyAdmin(admin.ModelAdmin):
    pass
