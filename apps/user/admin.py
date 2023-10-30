from django.contrib import admin
from apps.user.models import BaseUserModel
from django.contrib.auth.models import Group


@admin.register(BaseUserModel)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')

    def get_queryset(self, request):
        qs = super(BaseUserAdmin, self).get_queryset(request)
        return qs.filter(is_staff=True)
    exclude = ('user_type', 'groups')


admin.site.unregister(Group)
