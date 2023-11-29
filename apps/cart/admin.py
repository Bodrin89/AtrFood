from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.cart.models import CartModel, CartItem



@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity_product', 'sum_products', 'gifts')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)
