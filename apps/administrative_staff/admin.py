from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from apps.administrative_staff.models import AdministrativeStaffModel
from apps.user.admin import UserCreationForm

from django.contrib.auth.models import Group


@admin.register(AdministrativeStaffModel)
class AdministrativeStaffAdmin(admin.ModelAdmin):
    ordering = ('email',)
    list_display = ('id', 'email')
    search_fields = ('id', 'email')
    exclude = ('password',)

    def add_view(self, request, form_url="", extra_context=None):
        self.form = UserCreationForm
        return super().add_view(request, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)



@admin.register(Group)
class AdministrativeStaffAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)