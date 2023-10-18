from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.company_user.models import CompanyUserModel, ContactPersonModel


@admin.register(ContactPersonModel)
class CompanyUser(TranslationAdmin):
    pass


@admin.register(CompanyUserModel)
class CompanyUser(TranslationAdmin):
    pass
