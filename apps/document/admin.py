from django.contrib import admin

from apps.document.models import DocumentModel


@admin.register(DocumentModel)
class DocumentAdmin(admin.ModelAdmin):
    pass
