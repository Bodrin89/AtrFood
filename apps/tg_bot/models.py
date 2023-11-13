from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import BaseUserModel


class BotModel(models.Model):
    class Meta:
        verbose_name = _('Телеграм бот')
        verbose_name_plural = _('Телеграм боты')

    chat_id = models.PositiveIntegerField(verbose_name=_('Чат id телеграм бота'))
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name='bot',
                             verbose_name=_('Пользователь'))
