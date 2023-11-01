from django.db import models
from apps.library.models import CountryManufacturer, ManufacturingCompany, PackageType
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from apps.user.models import BaseUserModel


class CatalogModel(models.Model):
    """Модель каталога категорий товара"""
    class Meta:
        verbose_name = _('Каталог товаров')
        verbose_name_plural = _('Каталоги товаров')

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CategoryProductModel(models.Model):
    """Модель категорий товара"""
    class Meta:
        verbose_name = _('Категория товара')
        verbose_name_plural = _('Категории товаров')

    name = models.CharField(max_length=255)
    catalog = models.ForeignKey(CatalogModel, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class SubCategoryProductModel(models.Model):
    """Модель подкатегории товара"""
    class Meta:
        verbose_name = _('Подкатегория товара')
        verbose_name_plural = _('Подкатегории товаров')

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    """Модель товара"""
    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')

    name = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('Наименование товара'))
    price = models.FloatField(verbose_name=_('Стоимость за единицу'))
    article = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Артикул товара'))
    discount_price = models.FloatField(blank=True, null=True, verbose_name=_('Цена с учетом скидки'))
    quantity_stock = models.IntegerField(verbose_name=_('Количество на складе'))
    rating = models.IntegerField(default=0, verbose_name=_('Рейтинг товара'))
    opt_quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Количество товара для ОПТа"))
    opt_price = models.FloatField(null=True, blank=True, verbose_name=_("ОПТовая цена за единицу товара"))
    existence = models.BooleanField(null=True, blank=True, default=True, verbose_name=_('Наличие товара на складе'))
    date_create = models.DateField(auto_now_add=True, verbose_name=_("Дата создания товара"))
    is_active = models.BooleanField(default=True, verbose_name=_("Товар активный/скрытый"))
    reviewed = models.BooleanField(verbose_name=_('Наличие отзывов у продукта'), default=False)
    subcategory = models.ForeignKey(
        SubCategoryProductModel,
        on_delete=models.CASCADE,
        verbose_name=_('Подкатегория товара'),
        related_name='products'
    )

    def __str__(self):
        return self.name


class DescriptionProductModel(models.Model):
    """Модель описания товара"""

    class Meta:
        verbose_name = _('Описание товара')
        verbose_name_plural = _('Описания товаров')

    manufacturer = models.ForeignKey(
        ManufacturingCompany,
        on_delete=models.PROTECT,
        verbose_name=_('Компания производитель')
    )
    made_in = models.ForeignKey(CountryManufacturer, on_delete=models.PROTECT, verbose_name=_('Страна изготовитель'))
    description = models.TextField(verbose_name=_('Описание товара'))
    package = models.ForeignKey(PackageType, on_delete=models.PROTECT, verbose_name=_('Формат упаковки'))
    product = models.OneToOneField(
        ProductModel,
        on_delete=models.CASCADE,
        related_name='product_data',
        null=True,
        verbose_name=_('Данные товара')
    )

    def __str__(self):
        return f'{self.manufacturer}'


class ProductImage(models.Model):
    product = models.ForeignKey(ProductModel, related_name='images', on_delete=models.CASCADE, verbose_name='Продукт')
    image = models.ImageField(upload_to='product/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return f'Изображение {self.image}'


class FavoriteProductModel(models.Model):
    """Модель избранных товаров"""
    class Meta:
        verbose_name = _('Избранный товар')
        verbose_name_plural = _('Избранные товары')

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product


class CompareProductModel(models.Model):
    """Модель товаров для сравнения"""
    class Meta:
        verbose_name = _('Товар для сравнения')
        verbose_name_plural = _('Товары для сравнения')

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product


@receiver(pre_save, sender=ProductModel)
def update_product_existence(sender, instance, **kwargs):
    if instance.quantity_stock == 0:
        instance.existence = False
    else:
        instance.existence = True
