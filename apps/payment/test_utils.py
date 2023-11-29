import json
import os

import requests
from dotenv import load_dotenv

from config.settings import LOGGER

load_dotenv()

"""
ORDER_EXPIRED: Создается после истечения срока действия заказа. Статус заказа: EXPIRED.
PAYMENT_DECLINED: Создается после неуспешной авторизации платежа. Статус платежа: DECLINED.
PAYMENT_APPROVED: Создается после успешной авторизации двухстадийного платежа. Статус платежа: APPROVED.
PAYMENT_CAPTURED: Создается после успешного списания платежа. Статус платежа: CAPTURED.
PAYMENT_CANCELED: Создается после успешной отмены авторизованного платежа. Статус платежа CANCELLED.
CARD_APPROVED: Создается после успешной верификации карты. Статус карты APPROVED.
CARD_DECLINED: Создается после неуспешной верификации карты. Статус карты DECLINED.
"""

API_KEY = os.getenv('PAYMENT_API_KEY')
URL_CREATE_WEBHOOK = "https://stage-api.ioka.kz/v2/webhooks"
URL_DELETE_WEBHOOK = "https://stage-api.ioka.kz/v2/webhooks/"
URL_GET_ALL_WEBHOOK = "https://stage-api.ioka.kz/v2/webhooks"



def create_webhook(*args):
    print(args)
    headers = {
        'API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }

    url_create_webhook = URL_CREATE_WEBHOOK

    data = {
        # "url": "https://43b2-94-43-3-29.ngrok-free.app/ru/api/payment/webhook/payment/3jhghj7fg6d3",
        "url": "https://artfood.dev.thefactory.kz/ru/api/payment/webhook/payment/3jhghj7fg6d3",
        "events": args
    }

    response = requests.post(url_create_webhook, headers=headers, data=json.dumps(data))

    print(response.json())

def get_all_webhooks():
    """Получение всех webhook-ов магазина"""
    url = URL_GET_ALL_WEBHOOK
    headers = {
        'API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    print(response.json())


def delete_webhook(webhook_id):

    url = URL_DELETE_WEBHOOK + str(webhook_id)
    headers = {
        'API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.delete(url, headers=headers)

    print(response.status_code)


# delete_webhook("whk_4qLJU4B1aO")
# create_webhook("ORDER_EXPIRED", "PAYMENT_DECLINED", "PAYMENT_CAPTURED", "CARD_DECLINED")
# get_all_webhooks()

