# Generated by Django 4.2.5 on 2023-10-10 14:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_alter_productmodel_quantity_stock'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReviewProductView',
            new_name='ReviewProductModel',
        ),
    ]
