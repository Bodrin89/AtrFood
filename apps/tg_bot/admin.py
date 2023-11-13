from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.tg_bot.models import BotMessage


@admin.register(BotMessage)
class BotMassageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not BotMessage.objects.exists()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)
