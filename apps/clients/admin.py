from django.contrib import admin
from apps.user.models import AddressModel, BaseUserModel
from apps.order.models import Order


class ClientUserProxy(BaseUserModel):
    class Meta:
        proxy = True
        app_label = "clients"
        verbose_name = 'Клиент'
        verbose_name_plural = "Клиенты"


class OrderInline(admin.StackedInline):
    model = Order
    fk_name = "user"
    ordering = ['-date_created']
    extra = 0
    exclude = ('payment_date', 'total_quantity')


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
    inlines = [AddressInline, OrderInline]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'user_type')