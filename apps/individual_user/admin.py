from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.individual_user.models import IndividualUserModel
from apps.order.models import Order
from apps.user.models import AddressModel


class OrderInline(admin.StackedInline):
    model = Order
    fk_name = 'user'
    ordering = ['-date_created']
    extra = 0
    exclude = ('payment_date', 'total_quantity')


class AddressInline(admin.TabularInline):
    model = AddressModel
    max_num = 0


@admin.register(IndividualUserModel)
class IndividualUserAdmin(TranslationAdmin):
    list_display = ['email', 'phone_number', 'username']
    inlines = [AddressInline, OrderInline]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'user_type')
