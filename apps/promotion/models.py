from django.core.mail import send_mail
from django.db import models, transaction
from django.db.models import F, Q
from django.db.models.signals import m2m_changed, post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.product.models import ProductModel, SubCategoryProductModel
from apps.promotion.tasks import send_email_promotion
from config.settings import LOGGER


class Gift(models.Model):
    """Модель подарков"""

    class Meta:
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'

    name = models.CharField(max_length=255, verbose_name='Название подарка')
    description = models.TextField(blank=True, null=True, verbose_name='Описание подарка')


class DiscountModel(models.Model):
    """Модель конструктора акций"""

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    ACTION_TYPE_CHOICES = [
        ('discount', _('Скидка')),
        ('gift', _('Подарок')),
    ]

    name = models.CharField(max_length=255, verbose_name='Наименование акции')
    image = models.ImageField(upload_to='media', null=True, blank=True, verbose_name="фото акции")
    is_show = models.BooleanField(default=True, verbose_name="вывод на фронт")
    subcategory_product = models.ForeignKey(SubCategoryProductModel, null=True, blank=True, on_delete=models.CASCADE,
                                            verbose_name='Скидка для всей подкатегории товара')
    product = models.ManyToManyField(ProductModel, related_name='products', verbose_name='товары по акции')
    use_limit_sum_product = models.BooleanField(default=True, verbose_name='Учитывать лимит по сумме товара в корзине')
    limit_sum_product = models.FloatField(default=0, verbose_name='Сумма товара в корзине после которой действует '
                                                                  'акция')
    count_person = models.PositiveIntegerField(default=0, verbose_name='количество человек воспользовавшихся акцией')
    count_product = models.PositiveIntegerField(default=0, verbose_name='количество купленных товаров по акции')
    use_limit_person = models.BooleanField(default=True, verbose_name='Учитывать лимит по количеству человек')
    limit_person = models.PositiveIntegerField(verbose_name='Ограничение по количеству человек')
    use_limit_product = models.BooleanField(default=True, verbose_name='Учитывать лимит по количеству товара')
    limit_product = models.PositiveIntegerField(verbose_name='Ограничение по количеству товара')
    use_limit_loyalty = models.BooleanField(default=True, verbose_name='Учитывать систему лояльности')
    date_end_discount = models.DateField(verbose_name='Дата окончания акции')
    is_active = models.BooleanField(default=True, verbose_name='Действующая/архивная акция')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES, verbose_name='Тип акции')
    discount_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Размер скидки')
    gift = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Подарок')

    def save(self, created=False, *args, **kwargs):
        """При создании новой акции, отправляется письмо с названием акции"""
        created = not bool(self.pk)
        super().save(*args, **kwargs)
        if created:
            # send_email_promotion.apply_async(args=[self.name])
            pass

    def __str__(self):
        return self.name


class LoyaltyModel(models.Model):
    """Модель системы лояльности"""

    class Meta:
        verbose_name = 'Система лояльности'
        verbose_name_plural = 'Системы лояльности'

    LEVEL_LOYALTY = [
        ('bronze', _('бронза')),
        ('silver', _('серебро')),
        ('gold', _('золото')),
        ('platinum', _('платина')),
    ]

    level = models.CharField(max_length=10, choices=LEVEL_LOYALTY, verbose_name='Уровень лояльности')
    discount_percentage = models.PositiveSmallIntegerField(verbose_name='Процент скидки')
    sum_step = models.PositiveIntegerField(verbose_name='Порог цены')

    def __str__(self):
        return self.level


@receiver(post_save, sender=DiscountModel)
def apply_discount_to_products(instance, sender, **kwargs):
    """Обработчик события создания скидки"""
    prod = DiscountModel.objects.all()
    all_products = change_discount_price(prod)
    # instance_prod = set().union(all_products['dict_products'].get(instance))
    # instance.product.add(*instance_prod)
    try:
        instance_prod = set().union(all_products['dict_products'].get(instance))
        instance.product.add(*instance_prod)
    except Exception as e:
        LOGGER.error(f'error{e}')
        pass


@receiver(m2m_changed, sender=DiscountModel.product.through)
def update_discount_price(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Обработчик события изменения скидки при удалении какого-то продукта из скидки"""
    prod = DiscountModel.objects.all()
    all_products = change_discount_price(prod)
    if action == 'post_add':
        # add_prod = instance.product.all()
        for item in all_products['all_products']:
            discounts = get_discount(item)
            discount_amounts = [discount.discount_amount for discount in discounts]
            item.discount_price = get_sum_price_product(item.price, discount_amounts)
            item.save()
    if action == 'post_remove':
        try:
            instance_prod = set().union(all_products['dict_products'].get(instance))
            instance.product.add(*instance_prod)
        except Exception as e:
            LOGGER.error(f'error{e}')
            pass

        removed_products = ProductModel.objects.filter(pk__in=pk_set)
        not_remove_product = []
        for discount in prod:
            products = discount.product.all()
            not_remove_product.append(products)
        product = [item for sublist in not_remove_product for item in sublist]
        for item in removed_products:
            if item not in product:
                item.discount_price = None
                item.save()


@receiver(pre_delete, sender=DiscountModel)
def delete_products(sender, instance, **kwargs):
    """Сбрасывание цены со скидкой у товара при удалении скидки"""
    prod = DiscountModel.objects.all()
    all_products = change_discount_price(prod)
    for item in all_products['all_products']:
        discounts = get_discount(item)
        discount_amounts = [discount.discount_amount for discount in discounts if discount != instance]
        item.discount_price = get_sum_price_product(item.price, discount_amounts)
        if item.discount_price == item.price:
            item.discount_price = None
        item.save()


def change_discount_price(prod):
    """Изменение цены со скидкой"""
    products = []
    dict_products = {}
    for discount in prod:
        if product := discount.product.all():
            products.append(product)
            dict_products[discount] = product
        try:
            if subcategory_product := discount.subcategory_product.products.all():
                products.append(subcategory_product)
                dict_products[discount] = subcategory_product
        except Exception as e:
            LOGGER.error(f'error {e}')
            pass
    all_products = set().union(*products)
    return {'dict_products': dict_products, 'all_products': all_products}


def get_discount(product: ProductModel) -> list[DiscountModel]:
    """Фильтр акций по условиям"""
    discounts = product.products.all().filter(is_active=True)
    return discounts


def get_sum_price_product(price, discount_amounts):
    """Расчет суммы товаров в корзине с учетом всех скидок"""
    # return price - (price * sum(discount_amounts)) / 100
    return price - (price * sum(filter(None, discount_amounts))) / 100

