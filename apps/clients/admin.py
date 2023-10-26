from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from apps.order.models import Order
from apps.clients.models import AddressModel
from apps.user.models import BaseUserModel


class ClientUserProxy(BaseUserModel):
    class Meta:
        proxy = True
        app_label = 'clients'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


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
    max_num = 0


@admin.register(AddressModel)
class AddressModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientUserProxy)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number', 'username']

    def get_queryset(self, request):
        qs = super(ClientUserAdmin, self).get_queryset(request)
        return qs.filter(is_staff=False)

    def has_add_permission(self, request):
        return False

    inlines = [AddressInline, OrderInline]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser')
    readonly_fields = ('user_type', )
