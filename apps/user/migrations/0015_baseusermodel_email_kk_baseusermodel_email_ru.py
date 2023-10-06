# Generated by Django 4.2.5 on 2023-10-06 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_remove_baseusermodel_email_kk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseusermodel',
            name='email_kk',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='baseusermodel',
            name='email_ru',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
