from django.contrib import admin
from apps.order.models import Order, OrderItem, DeliveryAddress
from django.utils.translation import gettext_lazy as _


class DeliveryAddressInline(admin.StackedInline):
    model = DeliveryAddress
    # extra = 1
    # max_num = 1
    # readonly_fields = ('get_product_price', 'product', 'quantity', 'price')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    # max_num = 1
    # readonly_fields = ('get_product_price', 'product', 'quantity', 'price')
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
