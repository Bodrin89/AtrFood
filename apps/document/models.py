from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentModel(models.Model):
    """Модель документов"""

    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Документы")

    file = models.FileField(upload_to='documents', null=True, blank=True)

