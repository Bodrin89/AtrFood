from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.user.models import BaseUserModel, RegionModel, AddressModel


@admin.register(RegionModel)
class RegionAdmin(TranslationAdmin):
    pass


@admin.register(BaseUserModel)
class BaseUserAdmin(TranslationAdmin):
    pass


@admin.register(AddressModel)
class AddressAdmin(TranslationAdmin):
    pass