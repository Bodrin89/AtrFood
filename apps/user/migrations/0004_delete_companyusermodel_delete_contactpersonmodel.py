# Generated by Django 4.2.5 on 2023-10-05 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_delete_individualusermodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CompanyUserModel',
        ),
        migrations.DeleteModel(
            name='ContactPersonModel',
        ),
    ]