from django.db import models

from apps.product.models import ProductModel


class ReviewProductView(models.Model):
    class Meta:
        verbose_name = 'Отзыв на товар'
        verbose_name_plural = 'Отзывы на товары'

    class Stars(models.TextChoices):
        ONE_STAR = 1
        TWO_STAR = 2
        THREE_STAR = 3
        FOUR_STAR = 4
        FIVE_STAR = 5

    count_stars = models.CharField(max_length=1, choices=Stars.choices, default=None, verbose_name="количество звезд")
    review_text = models.TextField(blank=True, null=True, verbose_name="отзыв")
    foto = models.ImageField(blank=True, null=True, upload_to='media', verbose_name="фото")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
