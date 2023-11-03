from django.contrib import admin
from apps.blog.models import Blog, BlogImage
from modeltranslation.admin import TranslationAdmin


class BlogImageInline(admin.StackedInline):
    model = BlogImage
    extra = 0


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ['id', 'theme']
    inlines = [BlogImageInline, ]
