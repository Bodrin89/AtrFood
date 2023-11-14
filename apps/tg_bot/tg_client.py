
from django.core.cache import cache
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from apps.administrative_staff.models import AdministrativeStaffModel
from apps.library.models import AddressArtFood
from apps.order.models import Order
from apps.tg_bot import bot
from apps.tg_bot.models import BotModel
from apps.tg_bot.services import get_store_not_city_user, get_bot_message_cache, show_manager_menu, get_menu, \
    show_main_menu, show_registration_menu, check_order, get_order_from_text, check_status_order, change_status_order
from config.settings import TIME_CACHE_TG_BOT_MESSAGE, LOGGER


@bot.message_handler(commands=['start'])
def verify_user(message):
    """Проверка зарегистрирован пользователь или нет и является ли он менеджером"""
    try:
        user_bot = BotModel.objects.select_related('user').filter(chat_id=message.chat.id).first()
        if user_bot:
            # TODO добавить доп фильтры
            is_manager = AdministrativeStaffModel.objects.filter(baseusermodel_ptr_id=user_bot.user.id).first()
            if is_manager:
                bot.send_message(message.chat.id, f'{user_bot.user.username} вы вошли в аккаунт менеджера')
                show_manager_menu(message)
                get_menu(message)
            elif user_bot:
                introductory_message = get_bot_message_cache('introductory_message')
                bot.send_message(message.chat.id, f'{user_bot.user.username} {introductory_message}')
                show_main_menu(message)
                get_menu(message)
        else:
            show_registration_menu(message)
    except BotModel.DoesNotExist:
        pass


@bot.message_handler(content_types=['text'])
def get_button_menu(message: Message):
    user_bot = BotModel.objects.select_related('user').filter(chat_id=message.chat.id).first()
    if user_bot:
        # TODO добавить доп фильтры
        is_manager = AdministrativeStaffModel.objects.filter(baseusermodel_ptr_id=user_bot.user.id).first()
        if message.text == 'Меню' and is_manager:
            return show_manager_menu(message)
        return show_main_menu(message)
    return


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


@bot.callback_query_handler(func=lambda call: call.data == 'Взять в работу')
def take_order(call):
    """Если менеджер взял заказ в работу, статус заказа меняется на in_progress"""
    text = call.message.text
    order_id = get_order_from_text(text)
    order = check_status_order(order_id=order_id, chat_id=call.message.chat.id, message_id=call.message.message_id)
    if not order:
        return None
    bot_model_user = BotModel.objects.get(user_id=order.user_id)
    change_status_get_manager_name = change_status_order(order=order, chat_id=call.message.chat.id, order_id=order_id)
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)
    manager_name = change_status_get_manager_name.get('manager_name')
    LOGGER.debug(manager_name)
    bot.send_message(chat_id=bot_model_user.chat_id, text=f'Здравствуйте, {order.user.username}, я ваш менеджер меня '
                                                          f'зовут {manager_name} скоро я с вами '
                                                          f'свяжусь для уточнения деталей заказа')

    return bot.send_message(call.message.chat.id, f'Вы взяли в работу заказ с номером {order_id}')


@bot.callback_query_handler(func=lambda call: call.data == 'Отказаться')
def refuse_order(call):
    """Если менеджер отказался от заказа"""
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)


@bot.callback_query_handler(func=lambda call: call.data == 'заявки от клиентов')
def get_orders_users(call):
    """Просмотр заказов от клиентов"""
    orders_query_set = Order.objects.select_related('user').filter(status__in=['new_paid', 'new_unpaid'])
    if not orders_query_set:
        return bot.send_message(call.message.chat.id, text='Нет заказов для обработки')
    for item in orders_query_set:
        order_number = item.id
        markup_managers = InlineKeyboardMarkup()
        but1 = InlineKeyboardButton('Взять в работу', callback_data='Взять в работу без запроса')
        but2 = InlineKeyboardButton('Отказаться', callback_data='Отказаться')
        markup_managers.row(but1, but2)
        bot.send_message(call.message.chat.id, f'Заказ номер: {order_number}',
                         reply_markup=markup_managers)


@bot.callback_query_handler(func=lambda call: call.data == 'Взять в работу без запроса')
def take_order_manager(call):
    """Если менеджер взял заказ в работу, статус заказа меняется на in_progress"""
    order_id = get_order_from_text(call.message.text)
    order = check_status_order(order_id=order_id, chat_id=call.message.chat.id, message_id=call.message.message_id)
    if not order:
        return None
    change_status_order(order=order, chat_id=call.message.chat.id, order_id=order_id)
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)
    # bot.send_message(chat_id=bot_model_user.chat_id, text=f'Здравствуйте, {order.user.username}, я ваш менеджер меня '
    #                                                       f'зовут {manager_model_bot.user.username} скоро я с вами '
    #                                                       f'свяжусь для уточнения деталей заказа')

    return bot.send_message(call.message.chat.id, f'Вы взяли в работу заказ с номером {order_id}')
