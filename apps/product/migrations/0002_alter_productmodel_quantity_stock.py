# Generated by Django 4.2.5 on 2023-10-10 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='quantity_stock',
            field=models.IntegerField(verbose_name='количество на складе'),
        ),
    ]
