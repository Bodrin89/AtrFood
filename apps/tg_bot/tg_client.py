import json

import telebot
from telebot.apihelper import ApiTelegramException
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from apps.library.models import AddressArtFood
from apps.order.models import Order
from apps.tg_bot.models import BotModel
from apps.tg_bot.services import is_within_time_range, get_week_day, get_store_not_city_user
from apps.user.models import BaseUserModel
from config.settings import BOT_TOKEN, LOGGER

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def verify_user(message: Message):
    """Проверка зарегистрирован пользователь или нет и является ли он менеджером"""
    try:
        user_bot = BotModel.objects.select_related('user').filter(chat_id=message.chat.id).first()
        if user_bot and user_bot.user.is_superuser:
            bot.send_message(message.chat.id, f'{user_bot.user.username} вы вошли в аккаунт менеджера')
        elif user_bot:
            bot.send_message(message.chat.id, f'{user_bot.user.username} добро пожаловать в магазин ArtFood')
            show_main_menu(message)
            get_menu(message)
        else:
            show_registration_menu(message)
    except BotModel.DoesNotExist:
        pass


@bot.message_handler(content_types=['text'])
def get_button_menu(message: Message):
    if message.text == 'Меню':
        show_main_menu(message)
    return


def get_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = KeyboardButton('Меню')
    markup.add(but1)
    bot.send_message(message.chat.id, 'Меню:', reply_markup=markup)
    bot.register_next_step_handler(message, show_main_menu)


def show_registration_menu(message: Message) -> None:
    """Приветствие пользователя если он заходит в первый раз"""
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('cancel', callback_data='cancel')
    markup.row(but1)
    bot.send_message(message.chat.id, 'Добро пожаловать в магазин ArtFood\n'
                                      'Если вы не зарегистрированы, пройдите регистрацию на сайте\n'
                                      'Если вы зарегистрированы, введите ваш email\n'
                                      'Для отмены нажмите "cancel"', reply_markup=markup)
    bot.register_next_step_handler(message, check_email)


def show_main_menu(message: Message) -> None:
    """Меню для пользователя прошедшего верификацию"""
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Режим работы магазина', callback_data='markup1')
    but2 = InlineKeyboardButton('Магазины в других городах', callback_data='markup2')
    but3 = InlineKeyboardButton('Доставка заказанного товара', callback_data='markup3')
    markup.row(but3)
    markup.row(but1, but2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

######
def check_email(message: Message) -> None:
    """Функция принимает email от пользователя и проверяет есть ли такой пользователь"""
    if message.content_type != 'text':
        bot.send_message(message.chat.id, 'Не корректный тип данных')
        return show_registration_menu(message)
    if message.text.lower() == 'cancel':
        bot.send_message(message.chat.id, 'До свидания')
        return None
    if message.text.lower() in ['start', '/start']:
        return show_registration_menu(message)

    email = message.text
    try:
        user = BaseUserModel.objects.get(email=email, is_active=True)
        is_manager = user.is_superuser
        if is_manager:
            BotModel.objects.get_or_create(chat_id=message.chat.id, user=user)
            bot.send_message(message.chat.id,
                             f'Спасибо {user.username}, аккаунт подтвержден, вы вошли в чат менеджеров')
        else:
            BotModel.objects.get_or_create(chat_id=message.chat.id, user=user)
            bot.send_message(message.chat.id, f'Спасибо {user.username}  , аккаунт подтвержден')
            show_main_menu(message)
            get_menu(message)
    except BaseUserModel.DoesNotExist:
        bot.send_message(message.chat.id, 'Пользователя с таким email не существует')
        show_registration_menu(message)
    except BaseUserModel.MultipleObjectsReturned:
        bot.send_message(message.chat.id, 'Произошла ошибка. Обратитесь к администратору.')
######


# TODO рабочий функционал где манаджер это все суперпользаватели
# def check_email(message: Message) -> None:
#     """Функция принимает email от пользователя и проверяет есть ли такой пользователь"""
#     if message.content_type != 'text':
#         bot.send_message(message.chat.id, 'Не корректный тип данных')
#         return show_registration_menu(message)
#     if message.text.lower() == 'cancel':
#         bot.send_message(message.chat.id, 'До свидания')
#         return None
#     if message.text.lower() in ['start', '/start']:
#         return show_registration_menu(message)
#
#     email = message.text
#     try:
#         user = BaseUserModel.objects.get(email=email, is_active=True)
#         is_manager = user.is_superuser
#         if is_manager:
#             BotModel.objects.get_or_create(chat_id=message.chat.id, user=user)
#             bot.send_message(message.chat.id,
#                              f'Спасибо {user.username}, аккаунт подтвержден, вы вошли в чат менеджеров')
#         else:
#             BotModel.objects.get_or_create(chat_id=message.chat.id, user=user)
#             bot.send_message(message.chat.id, f'Спасибо {user.username}  , аккаунт подтвержден')
#             show_main_menu(message)
#             get_menu(message)
#     except BaseUserModel.DoesNotExist:
#         bot.send_message(message.chat.id, 'Пользователя с таким email не существует')
#         show_registration_menu(message)
#     except BaseUserModel.MultipleObjectsReturned:
#         bot.send_message(message.chat.id, 'Произошла ошибка. Обратитесь к администратору.')



    # try:
    #     # TODO можно будет удалить после тестов
    #     # Для физ и юр лиц
    #     # user = BaseUserModel.objects.filter(is_active=True, is_superuser=False).get(email=email)
    #     if user := BaseUserModel.objects.filter(is_active=True, is_superuser=False).get(email=email):
    #         BotModel.objects.get_or_create(chat_id=message.chat.id, user=user)
    #         bot.send_message(message.chat.id, f'Спасибо {user.username}  , аккаунт подтвержден')
    #         show_main_menu(message)
    #     else:
    #         # Для менеджеров
    #         LOGGER.debug('ff')
    #         user = BaseUserModel.objects.filter(is_active=True, is_superuser=True).get(email=email)
    #         user_manager_cat_id = BotModel.objects.select_related('user').filter(user__is_superuser=True)
    #         LOGGER.debug(f'**{user_manager_cat_id}')
    #         BotModel.objects.get_or_create(chat_id=message.chat.id, user=user)
    #         bot.send_message(message.chat.id, f'Спасибо {user.username}  , аккаунт подтвержден')
    #
    # except BaseUserModel.DoesNotExist:
    #     bot.send_message(message.chat.id, 'Пользователя с таким email не существует')
    #     show_registration_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def choice_cancel(call):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    but_start = KeyboardButton(text='start', )
    markup.row(but_start)
    bot.send_message(call.message.chat.id, 'До свидания', reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda call: call.data == 'markup1')
def get_open_store(call):
    user = BotModel.objects.filter(chat_id=call.message.chat.id).first().user
    user_addresses = user.addresses.all()
    if user_addresses:
        cities_user = [item.city.name for item in user_addresses]
        cities_store = AddressArtFood.objects.filter(
            city__name__in=cities_user).prefetch_related('open_store').all()
        work_time_store = get_store_not_city_user(cities_store, title='Магазины в вашем городе')
        bot.send_message(call.message.chat.id, f'Режим работы магазина\n{work_time_store}', parse_mode='HTML')
    else:

        cities_store = AddressArtFood.objects.prefetch_related('open_store').all()
        work_time_store = get_store_not_city_user(cities_store, title='Магазины во всех городах')
        bot.send_message(call.message.chat.id, f'Режим работы магазина\n{work_time_store}', parse_mode='HTML')


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
    response_text = get_store_not_city_user(cities_store, title='Магазины в других городах')
    bot.send_message(call.message.chat.id, text=response_text, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'markup3')
def delivery_order(call):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Да', callback_data='markup4'),
               InlineKeyboardButton('Нет', callback_data='markup5'))
    bot.send_message(call.message.chat.id, text='Вы заказывали товар в нашем магазине?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'markup4')
def ordering_yes(call):
    """Функция когда пользователь выбрал, что заказывал товар на сайте"""

    bot.send_message(call.message.chat.id, text='Введите номер заказа')
    bot.register_next_step_handler(call.message, check_order)


@bot.callback_query_handler(func=lambda call: call.data == 'markup5')
def ordering_no(call):
    """Отправляется сообщение если пользователь нажал что не заказывал товар на сайте"""
    bot.send_message(call.message.chat.id,
                     text="для того чтобы воспользоваться доставкой вам требуется приобрести товар на нашем сайте")


@bot.callback_query_handler(func=lambda call: call.data == 'markup6')
def ordering_no(call):
    """Отправляется сообщение если пользователь не желает ввести повторно номер заказа"""
    bot.send_message(call.message.chat.id, text="Выберете действие")
    show_main_menu(call.message)


def check_order(message: Message):
    """Проверка введенного пользователем номера заказа"""
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Да', callback_data='markup4'),
               InlineKeyboardButton('Нет', callback_data='markup6'))

    order_number = message.text

    if message.content_type != 'text' or not order_number.isdigit():
        bot.send_message(message.chat.id, text='Номер заказа  должен быть числом\n'
                                               'Попробовать снова?', reply_markup=markup)
        return
    user = BotModel.objects.filter(chat_id=message.chat.id).first().user
    order = Order.objects.get(user_id=user.id, id=order_number)

    if not order:
        bot.send_message(message.chat.id, text='Номер заказа не найден\n'
                                               'Попробовать снова?', reply_markup=markup)
        return

    formatted_day_of_week = get_week_day()
    user_addresses = user.addresses.all()
    cities_user = [item.city.name for item in user_addresses]
    cities_store = AddressArtFood.objects.filter(city__name__in=cities_user).prefetch_related('open_store').first()

    timezone = cities_store.city.timezone
    open_store = cities_store.open_store.all()
    res = {i.day: {'open': i.time_open.strftime("%H:%M:%S"), 'close': i.time_close.strftime("%H:%M:%S")} for i in
           open_store}

    work_time = res.get(formatted_day_of_week, {})

    if not work_time or not is_within_time_range(work_time.get('open'), work_time.get('close'), tz=timezone):
        bot.send_message(message.chat.id, text='Магазин закрыт, обратитесь в рабочее время')
        return

    chat_id_managers = BotModel.objects.select_related('user').filter(user__is_superuser=True)

    for item in chat_id_managers:
        chat_id = item.chat_id
        but1_data = {'b': '1', 'o': order_number}
        but2_data = {'b': '2', 'o': order_number}
        try:
            markup_managers = InlineKeyboardMarkup()
            but1 = InlineKeyboardButton('Взять в работу', callback_data=json.dumps(but1_data))
            but2 = InlineKeyboardButton('Отказаться', callback_data=json.dumps(but2_data))
            markup_managers.row(but1, but2)
            bot.send_message(chat_id=chat_id, text=f'Обработайте заказ номер: {order_number}',
                             reply_markup=markup_managers)
        except ApiTelegramException as e:
            """Обработка ошибки если номер заказа слишком большой и его не возможно передать в callback_data"""
            LOGGER.error(f'{e}, order_number: {but1_data.get("o")}')
    bot.send_message(message.chat.id, text=f'Ваш заказ обрабатывается')
    show_main_menu(message)


######### work mangers #######

@bot.callback_query_handler(func=lambda call: json.loads(call.data)['b'] == '1')
def take_order(call):
    """Если менеджер взял заказ в работу, статус заказа меняется на in_progress"""
    call_data = json.loads(call.data)
    order_id = call_data['o']
    order = Order.objects.select_related('user').get(id=order_id)
    if order.status not in ['new_paid', 'new_unpaid']:
        empty_markup = InlineKeyboardMarkup()
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=empty_markup)
        return bot.send_message(call.message.chat.id, text='Заказ взят в работу другим менеджером')
    bot_model_user = BotModel.objects.get(user_id=order.user_id)
    manager_model_bot = BotModel.objects.select_related('user').get(chat_id=call.message.chat.id)
    order.status = 'in_progress'
    order.save()
    ##### Удаление кнопоу после их нажатия
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)
    bot.send_message(chat_id=bot_model_user.chat_id, text=f'Здравствуйте, {order.user.username}, я ваш менеджер меня '
                                                          f'зовут {manager_model_bot.user.username} скоро я с вами '
                                                          f'свяжусь для уточнения заказа')
    return bot.send_message(call.message.chat.id, f'Вы взяли в работу заказ с номером {order_id}')


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['b'] == '2')
def refuse_order(call):
    """Если менеджер отказался от заказа"""
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)
