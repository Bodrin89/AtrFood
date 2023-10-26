from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from apps.user.models import BaseUserModel, RegionModel
from django.contrib.auth.models import Group


@admin.register(RegionModel)
class RegionAdmin(TranslationAdmin):
    pass


@admin.register(BaseUserModel)
class BaseUserAdmin(TranslationAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')

    def get_queryset(self, request):
        qs = super(BaseUserAdmin, self).get_queryset(request)
        return qs.filter(is_staff=True)
    exclude = ('user_type', 'region')


admin.site.unregister(Group)
