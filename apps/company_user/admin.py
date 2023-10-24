from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from apps.company_user.models import CompanyUserModel
from apps.order.models import Order
from apps.user.models import AddressModel


class OrderInline(admin.StackedInline):
    model = Order
    fk_name = 'user'
    ordering = ['-date_created']
    extra = 0
    readonly_fields = ['get_order_id', ]
    exclude = ('payment_date', 'total_quantity')

    def get_order_id(self, obj):
        return obj.id
    get_order_id.short_description = 'ID заказа'


class AddressInline(admin.TabularInline):
    model = AddressModel
    max_num = 0


@admin.register(CompanyUserModel)
class CompanyUserAdmin(TranslationAdmin):
    list_display = ['email', 'phone_number', 'username', 'company_name']
    inlines = [AddressInline, OrderInline]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'user_type')
