from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.promotion.models import DiscountModel


@admin.register(DiscountModel)
class DiscountAdmin(admin.ModelAdmin):
    pass