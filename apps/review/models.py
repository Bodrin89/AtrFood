from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

from apps.product.models import ProductModel
from apps.user.models import BaseUserModel


class ReviewProductModel(models.Model):
    """Модель отзыва"""
    class Meta:
        verbose_name = _('Отзыв на товар')
        verbose_name_plural = _('Отзывы на товары')

    class Stars(models.TextChoices):
        ONE_STAR = 1
        TWO_STAR = 2
        THREE_STAR = 3
        FOUR_STAR = 4
        FIVE_STAR = 5

    # count_stars = models.CharField(max_length=1, choices=Stars.choices, default=None, verbose_name='количество звезд')
    count_stars = models.PositiveIntegerField(choices=Stars.choices, default=0, verbose_name=_('Количество звезд'))
    review_text = models.TextField(blank=True, null=True, verbose_name=_('Отзыв'))
    foto = models.ImageField(blank=True, null=True, upload_to='media', verbose_name=_('Фото'))
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('Продукт'))
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, verbose_name=_('Пользователь'))

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        avg_rating = ReviewProductModel.objects.filter(product=self.product).aggregate(Avg('count_stars'))['count_stars__avg']
        self.product.rating = avg_rating
        self.product.save(update_fields=['rating'])
