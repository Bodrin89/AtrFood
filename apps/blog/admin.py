from django.contrib import admin
from apps.blog.models import Blog, BlogImage
from django.utils.translation import gettext_lazy as _


class BlogImageInline(admin.StackedInline):
    model = BlogImage
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'theme']
    inlines = [BlogImageInline, ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)