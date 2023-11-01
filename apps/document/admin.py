from django.contrib import admin

from apps.document.models import DocumentModel


class DocumentInline(admin.TabularInline):
    model = DocumentModel
    extra = 1

# @admin.register(DocumentModel)
# class DocumentAdmin(admin.ModelAdmin):
#     pass
