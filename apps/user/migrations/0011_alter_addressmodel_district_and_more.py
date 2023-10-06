# Generated by Django 4.2.5 on 2023-10-06 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_regionmodel_city_alter_regionmodel_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressmodel',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='addressmodel',
            name='house_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='addressmodel',
            name='street',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='baseusermodel',
            name='region',
            field=models.ForeignKey(default=32, on_delete=django.db.models.deletion.CASCADE, to='user.regionmodel'),
            preserve_default=False,
        ),
    ]
