from django.contrib import admin
from apps.blog.models import Blog, BlogImage


class BlogImageInline(admin.StackedInline):
    model = BlogImage
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'theme']
    inlines = [BlogImageInline, ]