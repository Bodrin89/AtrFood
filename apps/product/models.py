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
    # discount = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="скидка/старая цена товара")
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


class Gift(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название подарка')
    description = models.TextField(blank=True, null=True, verbose_name='Описание подарка')


class DiscountModel(models.Model):
    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    DISCOUNT_TYPE = 'discount'
    GIFT_TYPE = 'gift'

    ACTION_TYPE_CHOICES = [
        (DISCOUNT_TYPE, 'Скидка'),
        (GIFT_TYPE, 'Подарок'),
    ]

    name = models.CharField(max_length=255, verbose_name="Наименование акции")
    category_product = models.ForeignKey(CategoryProductModel, on_delete=models.CASCADE,
                                         verbose_name="Категория товара")
    product = models.ManyToManyField(ProductModel, related_name='products', verbose_name="товары по акции")
    sum_product = models.FloatField(verbose_name="Сумма товара в корзине")
    count_person = models.PositiveIntegerField(default=0, verbose_name="количество человек воспользовавшихся акцией")
    count_product = models.PositiveIntegerField(default=0, verbose_name="количество купленных товаров по акции")
    limit_person = models.PositiveIntegerField(verbose_name="Ограничение по количеству человек")
    limit_product = models.PositiveIntegerField(verbose_name="Ограничение по количеству товара")
    date_end_discount = models.DateField(verbose_name="Дата окончания акции")
    is_active = models.BooleanField(default=False, verbose_name="Действующая/архивная акция")
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES, verbose_name='Тип акции')
    discount_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Размер скидки')
    gift = models.ForeignKey('Gift', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Подарок')

