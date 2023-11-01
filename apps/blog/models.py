from django.db import models
from django.utils.translation import gettext_lazy as _


class Blog(models.Model):
    """Блог"""
    class Meta:
        verbose_name = _('Блог')
        verbose_name_plural = _('Блог')

    theme = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Тематика'))
    text = models.TextField(null=True, blank=True, verbose_name=_('Текст'))

    def __str__(self):
        return f'{self.theme}'


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name='images', on_delete=models.CASCADE, verbose_name='Медиа')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return f'Изображение {self.image}'
