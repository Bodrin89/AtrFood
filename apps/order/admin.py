from django.contrib import admin
from apps.order.models import Order, OrderItem, DeliveryAddress
from django.utils.translation import gettext_lazy as _


class DeliveryAddressInline(admin.StackedInline):
    model = DeliveryAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('get_product_price', )

    def get_product_price(self, obj):
        return obj.product.price
    get_product_price.short_description = _('Цена за единицу товара')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, DeliveryAddressInline]
    list_display = ['id', 'status', 'date_created']
    readonly_fields = ('returned', )
    list_editable = ('status',)
    search_fields = ('id',)
    list_filter = ('status', )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)
