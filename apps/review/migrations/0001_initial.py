# Generated by Django 4.2.5 on 2023-10-10 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewProductView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_stars', models.CharField(choices=[('1', 'One Star'), ('2', 'Two Star'), ('3', 'Three Star'), ('4', 'Four Star'), ('5', 'Five Star')], default=None, max_length=1, verbose_name='количество звезд')),
                ('review_text', models.TextField(blank=True, null=True, verbose_name='отзыв')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='media', verbose_name='фото')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отзыв на товар',
                'verbose_name_plural': 'Отзывы на товары',
            },
        ),
    ]
