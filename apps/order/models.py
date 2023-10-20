from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ExpressionWrapper, F, IntegerField, Sum
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.company_user.models import CompanyUserModel
from apps.individual_user.models import IndividualUserModel
from apps.product.models import ProductModel
from apps.promotion.models import LoyaltyModel
from apps.user.models import BaseUserModel
from apps.user.validators import validate_phone_number
from config.settings import LOGGER

User = get_user_model()


class Order(models.Model):
    """Модель заказа"""

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    ORDER_STATUS_CHOICES = [
        ('new_paid', 'Новые заказы оплаченные'),
        ('new_unpaid', 'Новые заказы не оплаченные'),
        ('in_progress', 'Заказы в обработке'),
        ('completed', 'Завершенные заказы'),
        ('returned', 'Возврат товара'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличный'),
        ('non_cash', 'Безналичный'),
        ('card', 'Оплата экварингом '),
    ]

    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='дата оплаты')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Покупатель', null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    delivery_address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    contact_phone = models.CharField(max_length=20, verbose_name='Номер телефона', validators=[validate_phone_number])
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, blank=True, null=True)
    total_quantity = models.PositiveIntegerField(verbose_name='Общее количество', blank=True, null=True)
    total_price = models.PositiveIntegerField(verbose_name='Общая стоимость', blank=True, null=True)
    payment_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Менеджер, ответственный за оплату',
        related_name='managed_orders',
        limit_choices_to={'is_staff': True}
    )

    def __str__(self):
        return f'Заказ {self.id} - {self.get_status_display()}'

    def save(self, *args, **kwargs):
        if not self.status:
            if self.payment_method == 'card':
                self.status = 'new_paid'
            else:
                self.status = 'new_unpaid'
        super(Order, self).save(*args, **kwargs)

    def update_totals(self):
        self.total_quantity = self.items.all().aggregate(Sum('quantity'))['quantity__sum'] or 0
        self.total_price = self.items.all().aggregate(Sum('price'))['price__sum'] or 0


class OrderItem(models.Model):
    """Модель товаров в заказе"""

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, verbose_name='Товар', null=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')
    price = models.PositiveIntegerField(verbose_name='Стоимость товара с учетом количества')

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_totals(sender, instance, **kwargs):
    instance.order.update_totals()


@receiver(post_save, sender=Order)
def update_level_loyalty(sender, instance, **kwargs):
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
