from django.contrib import admin
from apps.product.models import (
    CatalogModel,
    CategoryProductModel,
    DescriptionProductModel,
    ProductModel,
    SubCategoryProductModel,
    ProductImage,
)
from django.utils.translation import gettext_lazy as _


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class DescriptionProductInline(admin.StackedInline):
    model = DescriptionProductModel
    extra = 1
    exclude = ('logo',)


@admin.register(CatalogModel)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(CategoryProductModel)
class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'catalog',)
    search_fields = ('id', 'name')
    list_filter = ('catalog',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(SubCategoryProductModel)
class SubCategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category',)
    search_fields = ('id', 'name')
    list_filter = ('category',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'subcategory', 'reviewed', 'is_active')
    search_fields = ('id', 'name', 'article')
    list_filter = ('subcategory', 'reviewed')
    readonly_fields = ('rating', )
    inlines = (ProductImageInline, DescriptionProductInline)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)
