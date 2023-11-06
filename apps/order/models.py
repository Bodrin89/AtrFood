from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ExpressionWrapper, F, IntegerField, Sum
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from apps.company_user.models import CompanyUserModel
from apps.individual_user.models import IndividualUserModel
from apps.product.models import ProductModel
from apps.promotion.models import LoyaltyModel
from apps.user.models import BaseUserModel
from apps.clients.models import AddressModel
from apps.user.validators import validate_phone_number
from config.settings import LOGGER
from apps.library.models import City, District

User = get_user_model()


class Order(models.Model):
    """Модель заказа"""

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    ORDER_STATUS_CHOICES = [
        ('new_paid', _('Новые заказы оплаченные')),
        ('new_unpaid', _('Новые заказы не оплаченные')),
        ('in_progress', _('Заказы в обработке')),
        ('completed', _('Завершенные заказы')),
        ('returned', _('Возврат товара')),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', _('Наличный')),
        ('non_cash', _('Безналичный')),
        ('card', _('Оплата экварингом')),
    ]

    payment_date = models.DateTimeField(null=True, blank=True, verbose_name=_('дата оплаты'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name=_('Покупатель'), null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name=_('Метод оплаты'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    contact_phone = models.CharField(max_length=20, verbose_name=_('Номер телефона'),
                                     validators=[validate_phone_number])
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, blank=True, null=True,
                              verbose_name=_('Статус заказа'))
    total_quantity = models.PositiveIntegerField(verbose_name=_('Общее количество'), blank=True, null=True)
    total_price = models.PositiveIntegerField(verbose_name=_('Общая стоимость'), blank=True, null=True)
    payment_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Менеджер, ответственный за оплату'),
        related_name='managed_orders',
        limit_choices_to={'is_staff': True}
    )
    returned = models.BooleanField(default=False, verbose_name=_('Оформлен возврат'))

    def __str__(self):
        return f'Заказ №{self.id}'

    def save(self, *args, **kwargs):
        if not self.status:
            if self.payment_method == 'card':
                self.status = 'new_paid'
            else:
                self.status = 'new_unpaid'
        super(Order, self).save(*args, **kwargs)


class DeliveryAddress(models.Model):
    class Meta:
        verbose_name = _('Адрес доставки')
        verbose_name_plural = _('Адреса доставки')

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('Город'))
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_('Район'), blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Улица'))
    house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Номер дома'))
    apartment_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Номер квартиры'))
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Этаж'))
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery_address',
        verbose_name=_('Заказ')
    )

    def __str__(self):
        return f'{self.city}'


class OrderItem(models.Model):
    """Модель товаров в заказе"""

    class Meta:
        verbose_name = _('Товар в заказе')
        verbose_name_plural = _('Товары в заказе')

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_('Заказ'))
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, verbose_name=_('Товар'), null=True)
    quantity = models.PositiveIntegerField(verbose_name=_('Количество товара'))
    price = models.PositiveIntegerField(verbose_name=_('Стоимость товара с учетом количества'))
    gift = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, related_name='order_items_gift', null=True,
                             blank=True, verbose_name=_('Подарок'))

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_totals(sender, instance, **kwargs):
    order = instance.order
    order.total_quantity = order.items.all().aggregate(Sum('quantity'))['quantity__sum'] or 0
    order.total_price = order.items.all().aggregate(Sum('price'))['price__sum'] or 0
    order.save()


@receiver(post_save, sender=OrderItem)
def update_stock_on_orderitem_create(sender, instance, created, **kwargs):
    """Обновляем количество товара на складе после создания OrderItem."""
    if created:
        if instance.product.quantity_stock < instance.quantity:
            raise ValidationError(_(f"Недостаточно товара ") + f' {instance.product.name} ' + _(" на складе."))

        instance.product.quantity_stock = F('quantity_stock') - instance.quantity
        instance.product.save(update_fields=['quantity_stock', ])


@receiver(pre_save, sender=OrderItem)
def update_stock_on_orderitem_change(sender, instance, **kwargs):
    """Обновляем количество товара на складе при изменении OrderItem."""
    if instance.pk and instance.order.returned is not True:
        old_instance = OrderItem.objects.get(pk=instance.pk)

        old_quantity = old_instance.quantity
        new_quantity = instance.quantity
        if old_quantity != new_quantity:
            total_quantity = instance.product.quantity_stock
            total_quantity += old_quantity
            total_quantity -= new_quantity
            instance.product.quantity_stock = total_quantity
            instance.product.save(update_fields=['quantity_stock'])


@receiver(post_delete, sender=OrderItem)
def update_stock_delete_orderitem(sender, instance, **kwargs):
    """Обновляем количество товара на складе при удалении OrderItem."""
    if instance.order.returned is not True:
        instance.product.quantity_stock = F('quantity_stock') + instance.quantity
        instance.product.save(update_fields=['quantity_stock'])


@receiver(post_save, sender=Order)
def handle_returned_order(sender, instance, **kwargs):
    """Обновляем количество товара на складе если статус заказа возврат"""
    if instance.status == 'returned' and instance.returned is False:
        instance.returned = True
        for item in instance.items.all():
            product = item.product
            product.quantity_stock += item.quantity
            product.save()
        instance.save()


@receiver(post_save, sender=Order)
def update_level_loyalty(sender, instance, **kwargs):

    if instance.status == 'completed':
        user: BaseUserModel = User.objects.get(id=instance.user.id)
        loyalty = None

        if user.user_type == 'individual':
            user_model = IndividualUserModel
        elif user.user_type == 'company':
            user_model = CompanyUserModel
        else:
            return

        user_instance = user_model.objects.get(baseusermodel_ptr_id=user.id)
        sum_total_price = Order.objects.filter(user_id=user_instance.id,
                                               status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
        loyalty_levels = LoyaltyModel.objects.all().order_by('sum_step')
        for level in loyalty_levels:
            if level.sum_step > sum_total_price:
                break
            loyalty = level
        user_instance.loyalty = loyalty
        user_instance.save()
