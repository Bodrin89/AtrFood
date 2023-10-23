from datetime import timedelta

from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from apps.order.models import OrderItem
from apps.product.models import (CatalogModel,
                                 CategoryProductModel,
                                 DescriptionProductModel,
                                 ProductModel,
                                 SubCategoryProductModel,)
from apps.promotion.models import DiscountModel, LoyaltyModel
from django.db.models import Sum
from django.utils import timezone


@admin.register(CatalogModel)
class CatalogAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryProductModel)
class CategoryProductAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategoryProductModel)
class SubCategoryProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'subcategory',)
