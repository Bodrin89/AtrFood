import json
from django.urls import reverse

import telebot
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from apps.tg_bot.tg_client import bot


class TelegramWebhookView(APIView):

    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json.loads(json_str))
        bot.process_new_updates([update])
        return JsonResponse({'status': 'ok'})


# #TODO запуск телеграм бота с webhook, не забыть поменять url!!!
# bot.remove_webhook()
# bot.set_webhook(url=f'https://artfood.dev.thefactory.kz/4c3fd19b/')
