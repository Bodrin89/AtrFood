from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.individual_user.models import IndividualUserModel


@admin.register(IndividualUserModel)
class BaseUserAdmin(TranslationAdmin):
    pass


# from django.contrib import admin
# from apps.individual_user.models import IndividualUserModel
#
#
# @admin.register(IndividualUserModel)
# class IndividualUserAdmin(admin.ModelAdmin):
#     pass
