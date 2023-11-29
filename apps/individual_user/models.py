from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.promotion.models import LoyaltyModel
from apps.user.models import BaseUserModel


class IndividualUserModel(BaseUserModel):
    class Meta:
        verbose_name = _('Физическое лицо')
        verbose_name_plural = _('Физические лица')

    second_phone_number = models.CharField(max_length=20, null=True, blank=True,
                                           verbose_name=_('дополнительный номер телефона'))
    loyalty = models.ForeignKey(LoyaltyModel, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_('Уровень системы лояльности'))
