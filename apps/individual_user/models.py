from django.db import models

from apps.promotion.models import LoyaltyModel
from apps.user.models import BaseUserModel


class IndividualUserModel(BaseUserModel):
    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'

    second_phone_number = models.CharField(max_length=20, null=True, blank=True,
                                           verbose_name="дополнительный номер телефона")
    loyalty = models.ForeignKey(LoyaltyModel, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="Уровень системы лояльности")
