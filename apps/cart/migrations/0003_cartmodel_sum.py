# Generated by Django 4.2.5 on 2023-10-12 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartmodel_quantity_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartmodel',
            name='sum',
            field=models.FloatField(default=9999.0, verbose_name='сумма товаров в корзине'),
            preserve_default=False,
        ),
    ]