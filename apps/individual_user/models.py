from django.db import models

from apps.user.models import BaseUserModel


class IndividualUserModel(BaseUserModel):
    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'

    second_phone_number = models.CharField(max_length=20, null=True, blank=True,
                                           verbose_name="дополнительный номер телефона")
