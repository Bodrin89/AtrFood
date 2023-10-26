# Generated by Django 4.2.5 on 2023-10-26 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_productmodel_is_active'),
        ('order', '0005_alter_order_delivery_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='gift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items_gift', to='product.productmodel', verbose_name='Подарок'),
        ),
    ]
