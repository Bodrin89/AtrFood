from django.db import models

from apps.user.models import BaseUserModel


class CatalogModel(models.Model):
    """Модель каталога категорий товара"""
    class Meta:
        verbose_name = 'Каталог товаров'
        verbose_name_plural = 'Каталоги товаров'

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CategoryProductModel(models.Model):
    """Модель категорий товара"""
    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    name = models.CharField(max_length=255)
    catalog = models.ForeignKey(CatalogModel, on_delete=models.CASCADE, related_name='catalogs')

    def __str__(self):
        return self.name


class SubCategoryProductModel(models.Model):
    """Модель подкатегории товара"""
    class Meta:
        verbose_name = 'Подкатегория товара'
        verbose_name_plural = 'Подкатегории товаров'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class DescriptionProductModel(models.Model):
    """Модель описания товара"""
    class Meta:
        verbose_name = 'Описание товара'
        verbose_name_plural = 'Описания товаров'

    manufacturer = models.CharField(max_length=255, verbose_name='Компания производитель')
    made_in = models.CharField(max_length=255, verbose_name='Страна изготовитель')
    description = models.TextField(verbose_name='Описание товара')
    package = models.CharField(max_length=255, verbose_name='Формат упаковки')

    def __str__(self):
        return self.manufacturer


class ProductModel(models.Model):
    """Модель товара"""
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(null=True, blank=True, max_length=255, verbose_name='Наименование товара')
    foto = models.ImageField(null=True, blank=True, upload_to='media', verbose_name='Фото товара')
    price = models.FloatField(verbose_name='Стоимость за единицу')
    article = models.CharField(max_length=255, null=True, blank=True, verbose_name='Артикул товара')
    discount_price = models.FloatField(blank=True, null=True, verbose_name='Цена с учетом скидки')
    quantity_stock = models.IntegerField(verbose_name='Количество на складе')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг товара')
    # quantity_select = models.IntegerField(blank=True, null=True, verbose_name='выбор количества')
    existence = models.BooleanField(null=True, blank=True, default=True, verbose_name='Наличие товара на складе')
    product_data = models.ForeignKey(DescriptionProductModel, on_delete=models.CASCADE, verbose_name='Данные товара')
    subcategory = models.ForeignKey(SubCategoryProductModel, on_delete=models.CASCADE,
                                    verbose_name='Подкатегория товара', related_name='products')

    def __str__(self):
        return self.name


class FavoriteProductModel(models.Model):
    """Модель избранных товаров"""
    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product


class CompareProductModel(models.Model):
    """Модель товаров для сравнения"""
    class Meta:
        verbose_name = 'Товар для сравнения'
        verbose_name_plural = 'Товары для сравнения'

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product
