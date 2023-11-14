from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.order.models import Order
from apps.user.models import BaseUserModel


class AdministrativeStaffModel(BaseUserModel):
    class Meta:
        verbose_name = _('Административный персонал')
        verbose_name_plural = _('Административный персонал')

    class Role(models.TextChoices):
        ADMIN = ('admin', _('Администратор'))
        MAIN_MANAGER = ('main_manager', _('Главный менеджер'))
        REGIONAL_MANAGER = ('regional_manager', _('Региональный менеджер'))
        SUPERVISOR = ('supervisor', _('Руководитель'))
        CONTENT_MANAGER = ('content_manager', _('Контент менеджер'))

    role = models.CharField(max_length=25, choices=Role.choices, default=Role.CONTENT_MANAGER,
                            verbose_name=_('Роль'))
    order_in_work = models.ManyToManyField(Order, blank=True, related_name='administrative_staff',
                                           verbose_name=_('Заказы в работе'))
    # order_in_work = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True,
    #                                   related_name='administrative_staff')
