from functools import partial

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.company_user.models import CompanyUserModel
from apps.order.models import Order
from config.utils import upload_to_folder_path


class AvrFileModel(models.Model):
    class Meta:
        verbose_name = _("Документ АВР")
        verbose_name_plural = _("Документы АВР")

    company_user_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='file_avr')
    file_avr = models.FileField(
        upload_to=partial(upload_to_folder_path, folder_name='avr'),
        null=True, blank=True, verbose_name=_("Файл АВР"))

    def __str__(self):
        return f'{self.company_user_order.user}/{self.company_user_order}'


class DocumentModel(models.Model):
    """Модель документов"""

    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Документы")

    company_user = models.ForeignKey(CompanyUserModel, on_delete=models.CASCADE, related_name='document')
    file_avr = models.ForeignKey(AvrFileModel, on_delete=models.CASCADE, related_name='document', null=True, blank=True)
    file_payment_invoice = models.FileField(
        upload_to=partial(upload_to_folder_path, folder_name=f'payment_invoice'),
        null=True, blank=True, verbose_name=_("Файл счет на оплату"))

    def __str__(self):
        return f'{self.company_user}'

