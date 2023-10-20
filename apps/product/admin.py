

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.product.models import (CatalogModel,
                                 CategoryProductModel,
                                 DescriptionProductModel,
                                 ProductModel,
                                 SubCategoryProductModel,)
from apps.promotion.models import DiscountModel, LoyaltyModel


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
    pass


@admin.register(DescriptionProductModel)
class DescriptionProductAdmin(admin.ModelAdmin):
    pass
