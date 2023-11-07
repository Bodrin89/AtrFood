
from django.core.management import BaseCommand

from apps.tg_bot.tg_client import bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Запуск telegram-бота"""
        bot.infinity_polling()
