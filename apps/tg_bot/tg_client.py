import json

import telebot
from django.core.cache import cache
from telebot.apihelper import ApiTelegramException
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from apps.administrative_staff.models import AdministrativeStaffModel
from apps.library.models import AddressArtFood
from apps.order.models import Order
from apps.tg_bot.models import BotModel
from apps.tg_bot.services import is_within_time_range, get_week_day, get_store_not_city_user, check_open_store, \
    get_bot_message_cache
from apps.user.models import BaseUserModel
from config.settings import BOT_TOKEN, LOGGER, TIME_CACHE_TG_BOT_MESSAGE

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def verify_user(message: Message):
    """Проверка зарегистрирован пользователь или нет и является ли он менеджером"""
    try:
        user_bot = BotModel.objects.select_related('user').filter(chat_id=message.chat.id).first()
        if user_bot:
            # TODO добавить доп фильтры
            is_manager = AdministrativeStaffModel.objects.filter(baseusermodel_ptr_id=user_bot.user.id).first()
            if is_manager:
                bot.send_message(message.chat.id, f'{user_bot.user.username} вы вошли в аккаунт менеджера')
            elif user_bot:
                introductory_message = get_bot_message_cache('introductory_message')
                bot.send_message(message.chat.id, f'{user_bot.user.username} {introductory_message}')
                show_main_menu(message)
                get_menu(message)
        else:
            show_registration_menu(message)
    except BotModel.DoesNotExist:
        pass


# # TODO рабочий функционал где манаджер это все суперпользаватели
# @bot.message_handler(commands=['start'])
# def verify_user(message: Message):
#     """Проверка зарегистрирован пользователь или нет и является ли он менеджером"""
#     try:
#         user_bot = BotModel.objects.select_related('user').filter(chat_id=message.chat.id).first()
#         if user_bot and user_bot.user.is_superuser:
#             bot.send_message(message.chat.id, f'{user_bot.user.username} вы вошли в аккаунт менеджера')
#         elif user_bot:
#             bot.send_message(message.chat.id, f'{user_bot.user.username} добро пожаловать в магазин ArtFood')
#             show_main_menu(message)
#             get_menu(message)
#         else:
#             show_registration_menu(message)
#     except BotModel.DoesNotExist:
#         pass


@bot.message_handler(content_types=['text'])
def get_button_menu(message: Message):
    if message.text == 'Меню':
        show_main_menu(message)
    return


def get_menu(message):
    """Кнопка Меню для вывода основного меню"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = KeyboardButton('Меню')
    markup.add(but1)
    bot.send_message(message.chat.id, 'Меню', reply_markup=markup)


def show_registration_menu(message: Message) -> None:
    """Приветствие пользователя если он заходит в первый раз"""
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('cancel', callback_data='cancel')
    markup.row(but1)
    introductory_message_anonymous = get_bot_message_cache('introductory_message_anonymous')
    cache.set('introductory_message_user', introductory_message_anonymous, TIME_CACHE_TG_BOT_MESSAGE)
    bot.send_message(message.chat.id, text=introductory_message_anonymous, reply_markup=markup)
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
        is_manager = AdministrativeStaffModel.objects.filter(baseusermodel_ptr_id=user.id).first()
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
    message_order_not_site = get_bot_message_cache('message_order_not_site')
    cache.set('message_order_not_site', message_order_not_site, TIME_CACHE_TG_BOT_MESSAGE)
    bot.send_message(call.message.chat.id, text=message_order_not_site)


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
    user_bot = BotModel.objects.filter(chat_id=message.chat.id).first()
    if not user_bot:
        bot.send_message(chat_id=message.chat.id, text='Вы не подтвердили свой email')
        return show_registration_menu(message)
    user = user_bot.user
    order = Order.objects.filter(user_id=user.id, id=order_number).first()
    if not order:
        bot.send_message(message.chat.id, text='Номер заказа не найден\n'
                                               'Попробовать снова?', reply_markup=markup)
        return

    formatted_day_of_week = get_week_day()
    get_work_time = check_open_store(user, formatted_day_of_week)

    if not get_work_time:
        return bot.send_message(message.chat.id, text='У вас не зарегистрирован ни один адрес доставки')
    if not get_work_time['work_time'] or not is_within_time_range(get_work_time['work_time'].get('open'),
                                                                  get_work_time['work_time'].get('close'),
                                                                  tz=get_work_time.get('timezone')):
        message_after_hours = get_bot_message_cache('message_after_hours')
        cache.set('message_after_hours', message_after_hours, TIME_CACHE_TG_BOT_MESSAGE)
        return bot.send_message(message.chat.id, text=message_after_hours)

    managers = AdministrativeStaffModel.objects.filter(role__in=['content_manager'])
    chat_id_managers = BotModel.objects.select_related('user').filter(user_id__in=managers)

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
    manager = AdministrativeStaffModel.objects.get(baseusermodel_ptr_id=manager_model_bot.user.id)

    manager.order_in_work_id = order_id
    order.status = 'in_progress'
    manager.save()
    order.save()

    ##### Удаление кнопоу после их нажатия
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)
    bot.send_message(chat_id=bot_model_user.chat_id, text=f'Здравствуйте, {order.user.username}, я ваш менеджер меня '
                                                          f'зовут {manager_model_bot.user.username} скоро я с вами '
                                                          f'свяжусь для уточнения деталей заказа')

    return bot.send_message(call.message.chat.id, f'Вы взяли в работу заказ с номером {order_id}')


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['b'] == '2')
def refuse_order(call):
    """Если менеджер отказался от заказа"""
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)
