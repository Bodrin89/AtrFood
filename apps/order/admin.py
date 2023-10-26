from django.contrib import admin
from apps.order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    # max_num = 1
    # readonly_fields = ('get_product_price', 'product', 'quantity', 'price')
    readonly_fields = ('get_product_price', )

    def get_product_price(self, obj):
        return obj.product.price
    get_product_price.short_description = 'Цена за единицу товара'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'status', 'date_created']
    readonly_fields = ('returned', )
    list_editable = ('status',)
    search_fields = ('id',)
    list_filter = ('status', )
