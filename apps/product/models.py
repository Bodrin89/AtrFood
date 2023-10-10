from django.db import models

from apps.user.models import BaseUserModel


class CategoryProductModel(models.Model):
    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    name = models.CharField(max_length=255)


class SubCategoryProductModel(models.Model):
    class Meta:
        verbose_name = 'Подкатегория товара'
        verbose_name_plural = 'Подкатегории товаров'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE)


class ProductModel(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(null=True, blank=True, max_length=255, verbose_name="наименование товара")
    foto = models.ImageField(null=True, blank=True, upload_to='media', verbose_name="фото товара")
    price = models.FloatField(null=True, blank=True, verbose_name="стоимость за единицу")
    article = models.CharField(max_length=255, null=True, blank=True, verbose_name="артикул товара")
    discount = models.CharField(max_length=255, blank=True, null=True, verbose_name="скидка/старая цена товара")
    quantity_select = models.IntegerField(blank=True, null=True, verbose_name="выбор количества")
    existence = models.BooleanField(null=True, blank=True, default=True, verbose_name="наличие товара товара")
    description = models.TextField(null=True, blank=True, verbose_name="описание товара")
    category = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE, verbose_name="категория товара",
                                 null=True, blank=True)
    subcategory = models.ForeignKey(SubCategoryProductModel, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="подкатегория товара")


class FavoriteProductModel(models.Model):
    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'
        unique_together = ['user', 'product']

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE)


class ChosenProductModel(models.Model):
    class Meta:
        verbose_name = 'Товар для сравнения'
        verbose_name_plural = 'Товары для сравнения'

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE)
