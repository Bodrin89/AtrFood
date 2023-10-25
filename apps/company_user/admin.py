from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from apps.company_user.models import CompanyUserModel, ContactPersonModel, CompanyAddress
from apps.user.models import AddressModel
from apps.order.models import Order


class OrderInline(admin.StackedInline):
    model = Order
    fk_name = 'user'
    ordering = ['-date_created']
    extra = 0
    exclude = ('payment_date', 'total_quantity')


class AddressInline(admin.TabularInline):
    model = AddressModel
    max_num = 0


@admin.register(ContactPersonModel)
class ContactPersonModelAdmin(TranslationAdmin):
    pass


@admin.register(CompanyAddress)
class CompanyAddressAdmin(TranslationAdmin):
    pass


@admin.register(CompanyUserModel)
class CompanyUserAdmin(TranslationAdmin):
    list_display = ['email', 'phone_number', 'username', 'company_name']
    inlines = [AddressInline, OrderInline]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'user_type')

