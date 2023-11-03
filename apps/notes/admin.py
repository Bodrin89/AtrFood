from django.contrib import admin
from apps.notes.models import Note
from django.utils.translation import gettext_lazy as _


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', )
    search_fields = ('name', )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ('name',)
        return readonly_fields

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)