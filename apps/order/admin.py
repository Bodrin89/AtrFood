from django.contrib import admin

from apps.order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    max_num = 0
    readonly_fields = ('get_product_price', 'product', 'quantity', 'price')

    def get_product_price(self, obj):
        return obj.product.price
    get_product_price.short_description = 'Цена за единицу товара'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
