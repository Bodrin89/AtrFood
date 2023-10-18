from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.user.models import AddressModel, BaseUserModel, RegionModel


@admin.register(RegionModel)
class RegionAdmin(TranslationAdmin):
    pass


@admin.register(BaseUserModel)
class BaseUserAdmin(TranslationAdmin):
    pass


@admin.register(AddressModel)
class AddressAdmin(TranslationAdmin):
    pass
