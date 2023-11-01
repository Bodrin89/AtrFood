from django.contrib import admin
from apps.product.models import (
    CatalogModel,
    CategoryProductModel,
    DescriptionProductModel,
    ProductModel,
    SubCategoryProductModel,
    ProductImage,
)


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


@admin.register(CategoryProductModel)
class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'catalog',)
    search_fields = ('id', 'name')
    list_filter = ('catalog',)


@admin.register(SubCategoryProductModel)
class SubCategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category',)
    search_fields = ('id', 'name')
    list_filter = ('category',)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'subcategory', 'reviewed', 'is_active')
    search_fields = ('id', 'name', 'article')
    list_filter = ('subcategory', 'reviewed')
    readonly_fields = ('rating', )
    inlines = (ProductImageInline, DescriptionProductInline)
    # fieldsets = (
    #     ('Основная информация', {
    #         'fields': ('id', 'name', 'price'),
    #     }),
    #     ('Описание', {
    #         'fields': ('description_field',),
    #         'description': 'Здесь вы можете добавить дополнительное описание.'
    #     }),
    # )
