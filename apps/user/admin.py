from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.user.models import AddressModel, BaseUserModel, RegionModel


@admin.register(RegionModel)
class RegionAdmin(TranslationAdmin):
    pass


@admin.register(BaseUserModel)
class BaseUserAdmin(TranslationAdmin):
    def get_queryset(self, request):
        qs = super(BaseUserAdmin, self).get_queryset(request)
        return qs.filter(is_staff=True)
    exclude = ('user_type', 'region')
