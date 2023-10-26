from django.db import models
from django.db.models import Avg
from apps.product.models import ProductModel
from apps.user.models import BaseUserModel


class ReviewProductModel(models.Model):
    """Модель отзыва"""
    class Meta:
        verbose_name = 'Отзыв на товар'
        verbose_name_plural = 'Отзывы на товары'

    class Stars(models.IntegerChoices):
        ONE_STAR = 1, 'One Star'
        TWO_STAR = 2, 'Two Star'
        THREE_STAR = 3, 'Three Star'
        FOUR_STAR = 4, 'Four Star'
        FIVE_STAR = 5, 'Five Star'

    # count_stars = models.I(max_length=1, choices=Stars.choices, default=None, verbose_name='количество звезд')
    count_stars = models.PositiveIntegerField(choices=Stars.choices, default=0, verbose_name='Количество звезд')
    review_text = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Отзыв к продукту: {self.product}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        avg_rating = ReviewProductModel.objects.filter(product=self.product).aggregate(Avg('count_stars'))['count_stars__avg']
        self.product.rating = avg_rating
        self.product.save(update_fields=['rating'])


class ReviewImage(models.Model):
    review = models.ForeignKey(ReviewProductModel, related_name='images', on_delete=models.CASCADE, verbose_name='Продукт')
    image = models.ImageField(upload_to='review/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return f'Изображение {self.image}'
