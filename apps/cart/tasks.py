from django.utils import timezone

from apps.cart.models import CartModel
from config.celery import app


@app.task
def clear_old_cart():
    """Удаление старых корзин у которых нет пользователя"""
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    CartModel.objects.filter(user=None, created__lte=thirty_days_ago).delete()
