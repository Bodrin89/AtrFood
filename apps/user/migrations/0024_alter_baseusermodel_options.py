# Generated by Django 4.2.5 on 2023-10-23 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_alter_baseusermodel_managers_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseusermodel',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
