from django.db import models
from django.utils.translation import gettext_lazy as _


class Note(models.Model):
    text = models.TextField(blank=True, null=True, verbose_name=_('Текст'))
    name = models.CharField(max_length=50, verbose_name=_('Модель'))

    class Meta:
        verbose_name = _('Заметка')
        verbose_name_plural = _('Заметки')

    def __str__(self):
        return str(_(f"Заметка для модели {self.name}"))
