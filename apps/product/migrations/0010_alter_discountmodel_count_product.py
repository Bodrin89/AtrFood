# Generated by Django 4.2.5 on 2023-10-13 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_rename_limit_discount_discountmodel_limit_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountmodel',
            name='count_product',
            field=models.PositiveIntegerField(verbose_name='количество купленных товаров по акции'),
        ),
    ]
