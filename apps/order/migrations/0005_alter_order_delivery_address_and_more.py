# Generated by Django 4.2.5 on 2023-10-23 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_alter_baseusermodel_options'),
        ('order', '0004_alter_order_payment_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.addressmodel', verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличный'), ('non_cash', 'Безналичный'), ('card', 'Оплата экварингом ')], max_length=10, verbose_name='Метод оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('new_paid', 'Новые заказы оплаченные'), ('new_unpaid', 'Новые заказы не оплаченные'), ('in_progress', 'Заказы в обработке'), ('completed', 'Завершенные заказы'), ('returned', 'Возврат товара')], max_length=20, null=True, verbose_name='Статус заказа'),
        ),
    ]
