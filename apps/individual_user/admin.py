from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.urls import reverse
from django.utils.html import format_html
from apps.individual_user.models import IndividualUserModel
from apps.order.models import Order
from apps.clients.models import AddressModel


class OrderInline(admin.StackedInline):
    model = Order
    fk_name = 'user'
    ordering = ['-date_created']
    extra = 0
    exclude = ('total_quantity', )

    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,  instance._meta.model_name),  args=[instance.id])
        return format_html('<a href="{}">Просмотр заказа</a>', url)

    edit_link.short_description = 'Действие'
    readonly_fields = ('edit_link', 'returned')


class AddressInline(admin.TabularInline):
    model = AddressModel
    # max_num = 0
    extra = 1


@admin.register(IndividualUserModel)
class IndividualUserAdmin(TranslationAdmin):
    list_display = ['email', 'phone_number', 'username']
    inlines = [AddressInline, OrderInline]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'user_type', 'password')

