from time import sleep

from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.user.models import BaseUserModel
from config.settings import LOGGER, TIME_CACHE_TG_BOT_MESSAGE


class BotModel(models.Model):
    class Meta:
        verbose_name = _('Телеграм бот')
        verbose_name_plural = _('Телеграм боты')

    chat_id = models.PositiveIntegerField(verbose_name=_('Чат id телеграм бота'))
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name='bot',
                             verbose_name=_('Пользователь'))


class BotMessage(models.Model):
    class Meta:
        verbose_name = _('Сообщение телеграм бота')
        verbose_name_plural = _('Сообщения в телеграм боте')

    introductory_message = models.TextField(null=True,
                                            blank=True,
                                            help_text=_(
                                                'В начало сообщения автоматически подставляется имя пользователя'),
                                            verbose_name=_('вступительное сообщение'))
    message_after_hours = models.TextField(null=True, blank=True, verbose_name=_('сообщение в нерабочее время'))
    message_order_not_site = models.TextField(null=True, blank=True, verbose_name=_('сообщение заказ не через сайт'))
    introductory_message_anonymous = models.TextField(null=True, blank=True,
                                                      help_text=_('вместе с сообщением будет присылаться кнопка CANCEL '
                                                                  'для отмены подтверждения регистрации. Шаблон сообщения '
                                                                  'Добро пожаловать в магазин ArtFood. Если вы не '
                                                                  'зарегистрированы, пройдите регистрацию на сайте. Если вы '
                                                                  'зарегистрированы, введите ваш email. Для отмены '
                                                                  'нажмите "cancel"'),
                                                      verbose_name=_(
                                                          'вступительное сообщение для не зарегистрированного '
                                                          'пользователя'))


@receiver(post_save, sender=BotMessage)
def save_massage_in_cache(instance: BotMessage, sender, **kwargs):
    """Сохранение сообщений бота в кэш при изменении"""
    cache.set('introductory_message', instance.introductory_message, TIME_CACHE_TG_BOT_MESSAGE)
    cache.set('message_after_hours', instance.message_after_hours, TIME_CACHE_TG_BOT_MESSAGE)
    cache.set('message_order_not_site', instance.message_order_not_site, TIME_CACHE_TG_BOT_MESSAGE)
    cache.set('introductory_message_anonymous', instance.introductory_message_anonymous, TIME_CACHE_TG_BOT_MESSAGE)
