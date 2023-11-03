from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.urls import reverse
from django.utils.html import format_html
from apps.individual_user.models import IndividualUserModel
from apps.library.forms import AddressForm
from apps.order.models import Order
from apps.clients.models import AddressModel
from django.utils.translation import gettext_lazy as _
from django import forms


class OrderInline(admin.StackedInline):
    model = Order
    fk_name = 'user'
    ordering = ['-date_created']
    extra = 0
    exclude = ('total_quantity', )

    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,  instance._meta.model_name),  args=[instance.id])
        return format_html('<a href="{}">Просмотр заказа</a>', url)

    edit_link.short_description = 'Действие'
    readonly_fields = ('edit_link', 'returned')


class AddressInline(admin.TabularInline):
    form = AddressForm
    model = AddressModel
    # max_num = 0
    extra = 1


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = IndividualUserModel
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
        model = IndividualUserModel
        fields = "__all__"


@admin.register(IndividualUserModel)
class IndividualUserAdmin(TranslationAdmin):
    list_display = ['email', 'phone_number', 'username']
    inlines = [AddressInline, OrderInline]
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'user_type', 'password')

    def add_view(self, request, form_url="", extra_context=None):
        self.form = UserCreationForm
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.form = UserChangeForm
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)


