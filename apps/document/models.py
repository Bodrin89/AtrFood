from django.db import models
from django.utils.translation import gettext_lazy as _

from config.utils import upload_to_folder_path


class DocumentModel(models.Model):
    """Модель документов"""

    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Документы")

    file = models.FileField(
        upload_to=lambda instance, filename: upload_to_folder_path(instance, filename, 'company_user_docs'),
        null=True, blank=True)

    def __str__(self):
        return 'documents'

