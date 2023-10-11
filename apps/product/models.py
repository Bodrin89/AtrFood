from django.db import models

from apps.user.models import BaseUserModel


class CategoryProductModel(models.Model):
    """Модель категорий товара"""
    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    name = models.CharField(max_length=255)


class SubCategoryProductModel(models.Model):
    """Модель подкатегории товара"""
    class Meta:
        verbose_name = 'Подкатегория товара'
        verbose_name_plural = 'Подкатегории товаров'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE)


class DescriptionProductModel(models.Model):
    """Модель описания товара"""
    class Meta:
        verbose_name = 'Описание товара'
        verbose_name_plural = 'Описания товаров'

    manufacturer = models.CharField(max_length=255, verbose_name="Компания производитель")
    made_in = models.CharField(max_length=255, verbose_name="Страна изготовитель")
    description = models.TextField(verbose_name="Описание товара")
    package = models.CharField(max_length=255, verbose_name="Формат упаковки")


class ProductModel(models.Model):
    """Модель товара"""
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(null=True, blank=True, max_length=255, verbose_name="наименование товара")
    foto = models.ImageField(null=True, blank=True, upload_to='media', verbose_name="фото товара")
    price = models.FloatField(null=True, blank=True, verbose_name="стоимость за единицу")
    article = models.CharField(max_length=255, null=True, blank=True, verbose_name="артикул товара")
    discount = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="скидка/старая цена товара")
    discount_price = models.FloatField(blank=True, null=True, verbose_name="цена с учетом скидки")
    quantity_stock = models.IntegerField(verbose_name="количество на складе")
    quantity_select = models.IntegerField(blank=True, null=True, verbose_name="выбор количества") #TODO убрать
    existence = models.BooleanField(null=True, blank=True, default=True, verbose_name="наличие товара на складе")
    product_data = models.ForeignKey(DescriptionProductModel, on_delete=models.CASCADE, verbose_name="данные товара")
    category = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE, verbose_name="категория товара",
                                 null=True, blank=True)
    subcategory = models.ForeignKey(SubCategoryProductModel, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="подкатегория товара")


class FavoriteProductModel(models.Model):
    """Модель избранных товаров"""
    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)


class CompareProductModel(models.Model):
    """Модель товаров для сравнения"""
    class Meta:
        verbose_name = 'Товар для сравнения'
        verbose_name_plural = 'Товары для сравнения'

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
