# Generated by Django 4.2.5 on 2023-10-20 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_alter_categoryproductmodel_catalog_and_more'),
        ('promotion', '0008_alter_discountmodel_category_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discountmodel',
            name='category_product',
        ),
        migrations.AddField(
            model_name='discountmodel',
            name='subcategory_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.subcategoryproductmodel', verbose_name='Скидка для всей подкатегории товара'),
        ),
    ]
