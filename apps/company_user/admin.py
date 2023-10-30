from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from apps.company_user.models import CompanyUserModel, ContactPersonModel, CompanyAddress
from apps.clients.models import AddressModel
from apps.order.models import Order


class OrderInline(admin.StackedInline):
    model = Order
    fk_name = 'user'
    ordering = ['-date_created']
    extra = 0
    exclude = ('total_quantity', )

    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,  instance._meta.model_name),  args=[instance.id] )
        return format_html('<a href="{}">Просмотр заказа</a>', url)

    edit_link.short_description = 'Действие'
    readonly_fields = ('edit_link', 'returned')


class AddressInline(admin.TabularInline):
    model = AddressModel
    extra = 0


class CompanyAddressInline(admin.TabularInline):
    model = CompanyAddress
    extra = 0


@admin.register(ContactPersonModel)
class ContactPersonModelAdmin(TranslationAdmin):
    pass


@admin.register(CompanyUserModel)
class CompanyUserAdmin(TranslationAdmin):
    list_display = ['email', 'phone_number', 'username', 'company_name']
    inlines = [
        AddressInline,
        OrderInline,
        CompanyAddressInline
    ]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'user_type')

