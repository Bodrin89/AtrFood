# Generated by Django 4.2.5 on 2023-10-26 14:01

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0025_alter_baseusermodel_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientUserProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.baseusermodel',),
        ),
    ]
