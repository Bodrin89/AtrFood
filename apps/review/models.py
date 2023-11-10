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

    class Stars(models.IntegerChoices):
        ONE_STAR = 1, _('Одна звезда')
        TWO_STAR = 2, _('Две звезды')
        THREE_STAR = 3, _('Три звезды')
        FOUR_STAR = 4, _('Четыре звезды')
        FIVE_STAR = 5, _('Пять звезд')

    # count_stars = models.I(max_length=1, choices=Stars.choices, default=None, verbose_name='количество звезд')
    count_stars = models.PositiveIntegerField(choices=Stars.choices, default=0, verbose_name=_('Количество звезд'))
    review_text = models.TextField(blank=True, null=True, verbose_name=_('Отзыв'))
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('Продукт'))
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    date_created = models.DateField(auto_now=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Отзыв к продукту: {self.product}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        avg_rating = ReviewProductModel.objects.filter(product=self.product).aggregate(Avg('count_stars'))['count_stars__avg']
        self.product.rating = avg_rating
        self.product.reviewed = True
        self.product.save(update_fields=['rating', 'reviewed'])


class ReviewImage(models.Model):
    class Meta:
        verbose_name = _('Изображение товара')
        verbose_name_plural = _('Изображения товара')

    review = models.ForeignKey(ReviewProductModel, related_name='images', on_delete=models.CASCADE,
                               verbose_name=_('Товар'))
    image = models.ImageField(upload_to='review/', verbose_name=_('Изображение'), blank=True, null=True)

    def __str__(self):
        return f'Изображение {self.image}'
