# Generated by Django 4.2.5 on 2023-10-17 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0005_alter_discountmodel_gift'),
        ('individual_user', '0006_alter_individualusermodel_second_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualusermodel',
            name='loyalty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promotion.loyaltymodel', verbose_name='Уровень системы лояльности'),
        ),
    ]
