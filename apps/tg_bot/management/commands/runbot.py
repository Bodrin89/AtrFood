from django.core.management import BaseCommand

from apps.tg_bot.tg_client import bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Запуск telegram-бота"""
        bot.remove_webhook()
        bot.polling(non_stop=True)
    #
    # bot.remove_webhook()
    # bot.set_webhook(url=f'https://ba52-94-43-3-29.ngrok-free.app/4c3fd19b/')
