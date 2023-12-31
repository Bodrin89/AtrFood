from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.user.models import BaseUserModel
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = BaseUserModel
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = BaseUserModel
        fields = "__all__"


@admin.register(BaseUserModel)
class BaseUserAdmin(admin.ModelAdmin):

    ordering = ('email',)
    list_display = ('id', 'email')
    search_fields = ('id', 'email')

    def add_view(self, request, form_url="", extra_context=None):
        self.form = UserCreationForm
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.form = UserChangeForm
        return super().change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(BaseUserAdmin, self).get_queryset(request)
        return qs.filter(is_staff=True)
    exclude = ('user_type', 'groups', 'is_staff', 'password', 'permission_cart')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)


admin.site.unregister(Group)
