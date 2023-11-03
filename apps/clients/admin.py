from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, path
from django.utils.html import format_html

from apps.library.forms import AddressForm
from apps.order.models import Order
from apps.clients.models import AddressModel
from apps.user.models import BaseUserModel
from apps.product.models import ProductModel


class ClientUserProxy(BaseUserModel):
    class Meta:
        proxy = True
        app_label = 'clients'
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')


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
    form = AddressForm
    model = AddressModel
    # max_num = 0
    extra = 0


@admin.register(ClientUserProxy)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number', 'username']

    def get_queryset(self, request):
        qs = super(ClientUserAdmin, self).get_queryset(request)
        return qs.filter(is_staff=False)

    def has_add_permission(self, request):
        return False

    inlines = [AddressInline, OrderInline]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'password')
    readonly_fields = ('user_type', )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)
