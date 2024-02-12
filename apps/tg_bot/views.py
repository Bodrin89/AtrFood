import json
from django.urls import reverse

import telebot
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from apps.tg_bot.tg_client import bot
from config.settings import LOGGER


class TelegramWebhookView(APIView):

    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json.loads(json_str))
        bot.process_new_updates([update])
        return JsonResponse({'status': 'ok'})


#TODO запуск телеграм бота с webhook, не забыть поменять url!!!
# bot.remove_webhook()
# bot.set_webhook(url=f'https://api.artfood-shop.kz/4c3fd19b/')
# bot.set_webhook(url=f'https://9650-94-43-3-29.ngrok-free.app/4c3fd19b/')
# bot.set_webhook(url=f'https://0f6f-94-43-3-29.ngrok-free.app/4c3fd19b/')
