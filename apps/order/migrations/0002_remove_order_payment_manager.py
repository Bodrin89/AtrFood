# Generated by Django 4.2.5 on 2023-10-17 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_manager',
        ),
    ]
