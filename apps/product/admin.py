from django.contrib import admin
from apps.product.models import (
    CatalogModel,
    CategoryProductModel,
    DescriptionProductModel,
    ProductModel,
    SubCategoryProductModel,
    ProductImage,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


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


@admin.register(DescriptionProductModel)
class DescriptionProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'subcategory', 'reviewed', 'is_active')
    search_fields = ('id', 'name', 'article')
    list_filter = ('subcategory', 'reviewed')
    readonly_fields = ('rating', )
    inlines = (ProductImageInline,)

