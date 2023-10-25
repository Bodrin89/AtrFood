# Generated by Django 4.2.5 on 2023-10-16 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0002_loyaltymodel_discountmodel_use_limit_loyalty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountmodel',
            name='use_limit_sum_product',
            field=models.BooleanField(default=True, verbose_name='Учитывать лимит по сумме товара в корзине'),
        ),
        migrations.AlterField(
            model_name='discountmodel',
            name='sum_product',
            field=models.FloatField(default=0, verbose_name='Сумма товара в корзине после которой действует акция'),
        ),
    ]
