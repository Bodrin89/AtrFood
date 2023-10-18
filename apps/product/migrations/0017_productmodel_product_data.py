# Generated by Django 4.2.5 on 2023-10-18 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_remove_productmodel_product_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='product_data',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.descriptionproductmodel', verbose_name='данные товара'),
            preserve_default=False,
        ),
    ]