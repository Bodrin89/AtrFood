import json

import telebot

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from django.utils.translation import gettext_lazy as _

from apps.clients.models import AddressModel
from apps.library.models import AddressArtFood
from apps.tg_bot.models import BotModel
from apps.user.models import BaseUserModel
from config.settings import BOT_TOKEN, LOGGER

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def verify_user(message: Message):
    """Проверка зарегистрирован пользователь или нет"""
    try:
        user_bot = BotModel.objects.filter(chat_id=message.chat.id).first()
        if user_bot:
            bot.send_message(message.chat.id, f'{user_bot.user.username} добро пожаловать в магазин ArtFood')
            show_main_menu(message)
        else:
            show_registration_menu(message)

    except BotModel.DoesNotExist:
        pass


def show_registration_menu(message: Message) -> None:
    """Приветствие пользователя если он заходит в первый раз"""
    bot.send_message(message.chat.id, 'Добро пожаловать в магазин ArtFood\n'
                     'Если вы не зарегистрированы, пройдите регистрацию на сайте\n'
                     'Если вы зарегистрированы, введите ваш email\n'
                     'Для отмены введите "cancel"')
    bot.register_next_step_handler(message, check_email)


def show_main_menu(message: Message) -> None:
    """Меню для пользователя прошедшего верификацию"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Режим работы магазина', callback_data='markup1'))
    markup.add(InlineKeyboardButton('Магазины в других городах', callback_data='markup2'))
    markup.add(InlineKeyboardButton('Доставка заказанного товара', callback_data='markup3'))
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


def check_email(message: Message) -> None:
    """Функция принимает email от пользователя и проверяет есть ли такой пользователь"""
    if message.text == 'cancel':
        bot.send_message(message.chat.id, 'До свидания')
        return None
    email = message.text
    try:
        # TODO Улучшить условия поиска по пользователю
        user = BaseUserModel.objects.filter(is_active=True, is_superuser=False).get(email=email)
        BotModel.objects.get_or_create(chat_id=message.chat.id, user=user)
        bot.send_message(message.chat.id, f'Спасибо {user.username}  , аккаунт подтвержден')
        show_main_menu(message)

    except BaseUserModel.DoesNotExist:
        bot.send_message(message.chat.id, 'Пользователя с таким email не существует')
        show_registration_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == 'markup1')
def get_open_store(call):
    bot.send_message(call.message.chat.id, 'Режим работы магазина')


# @bot.callback_query_handler(func=lambda call: call.data == 'markup2')
# def get_store_other_city(call):
#     """Функция, которая отправляет пользователю город и режим работы магазинов не в его городе"""
#     user = BotModel.objects.filter(chat_id=call.message.chat.id).first().user
#     user_addresses = user.addresses.all()
#     if user_addresses:
#         cities_user = [item.city.name for item in user_addresses]
#         cities_store = AddressArtFood.objects.prefetch_related('open_store').exclude(city__name__in=cities_user)
#     else:
#         cities_store = AddressArtFood.objects.prefetch_related('open_store').all()
#
#     store_open_store = {}
#     for item in cities_store:
#         open_store = item.open_store.all()
#         res = {i.day: {'открывается': i.time_open.strftime("%H:%M:%S"),
#                        'закрывается': i.time_close.strftime("%H:%M:%S")} for i in open_store}
#         store_info = {
#             'район': item.district.name,
#             'улица': item.street,
#             'дом': item.house_number,
#             'офис': item.office_number if item.office_number else '-',
#             'режим работы магазина': res
#         }
#
#         store_key = f'{item.city.name}'
#         if store_key in store_open_store:
#             store_open_store[store_key].append(store_info)
#         else:
#             store_open_store[store_key] = [store_info]
#
#     json_data = json.dumps(store_open_store, indent=4, ensure_ascii=False)
#     bot.send_message(call.message.chat.id, text=f'<u>Магазины в других городах</u>\n{json_data}', parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'markup2')
def get_store_other_city(call):
    """Функция, которая отправляет пользователю город и режим работы магазинов не в его городе"""
    user = BotModel.objects.filter(chat_id=call.message.chat.id).first().user
    user_addresses = user.addresses.all()
    if user_addresses:
        cities_user = [item.city.name for item in user_addresses]
        cities_store = AddressArtFood.objects.prefetch_related('open_store').exclude(city__name__in=cities_user)
    else:
        cities_store = AddressArtFood.objects.prefetch_related('open_store').all()

    store_open_store = {}

    for item in cities_store:
        open_store = item.open_store.all()
        res = {i.day: {'открывается': i.time_open.strftime("%H:%M:%S"),
                       'закрывается': i.time_close.strftime("%H:%M:%S")} for i in open_store}
        store_info = {
            'район': item.district.name,
            'улица': item.street,
            'дом': item.house_number,
            'офис': item.office_number if item.office_number else '-',
            'режим работы магазина': res
        }

        city_key = item.city.name
        if city_key in store_open_store:
            store_open_store[city_key].append(store_info)
        else:
            store_open_store[city_key] = [store_info]

    response_text = "<u>Магазины в других городах</u>\n"

    for city, stores in store_open_store.items():
        response_text += f"\n<b>{city}</b>\n"
        for store_info in stores:
            response_text += "\n".join([f"{store_detail}: {value}" for store_detail, value in store_info.items()])
            response_text += "\n\n"
    bot.send_message(call.message.chat.id, text=response_text, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'markup3')
def delivery_order(call):

    bot.send_message(call.message.chat.id, 'Доставка заказанного товара')
