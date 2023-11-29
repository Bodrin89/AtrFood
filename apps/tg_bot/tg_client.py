from django.core.cache import cache
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from apps.administrative_staff.models import AdministrativeStaffModel
from apps.library.models import AddressArtFood, OpenStore
from apps.order.models import Order
from apps.tg_bot import bot
from apps.tg_bot.models import BotModel, BotMessage
from apps.tg_bot.services import get_store_not_city_user, get_bot_message_cache, show_manager_menu, get_menu, \
    show_main_menu, show_registration_menu, check_order, get_order_from_text, check_status_order, change_status_order, \
    get_menu_address_store, get_address_store, change_street, button_change_message, change_message, get_new_open_hours, \
    change_open_hours_store
from config.settings import TIME_CACHE_TG_BOT_MESSAGE, LOGGER

"""
Переменная TEXT является обязательной и ее нельзя менять.
tag это часть строки, перед числом которое надо достать из строки в TEXT
"""


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


@bot.callback_query_handler(func=lambda call: call.data == 'exit_manager_screen')
def exit_manager_screen(call):
    get_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'markup1')
def get_open_store(call):
    user = BotModel.objects.filter(chat_id=call.message.chat.id).first().user
    user_addresses = user.addresses.all()
    if user_addresses:
        cities_user = [item.city.name for item in user_addresses]
        cities_store = AddressArtFood.objects.filter(
            city__name__in=cities_user).prefetch_related('open_store').all()
        work_time_store = get_store_not_city_user(cities_store, title='Магазины в вашем городе')
        bot.send_message(call.message.chat.id, f'\n{work_time_store}',
                         parse_mode='HTML')
    else:
        cities_store = AddressArtFood.objects.prefetch_related('open_store').all()
        work_time_store = get_store_not_city_user(cities_store, title='Магазины во всех городах')
        bot.send_message(call.message.chat.id, f'\n{work_time_store}', parse_mode='HTML')


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
    tag = 'номер:'
    order_id = get_order_from_text(text=text, tag=tag)
    if order_id is None or not str(order_id).isdigit():
        return bot.send_message(call.message.chat.id, text='id магазина должно быть числом и не None')
    order = check_status_order(order_id=order_id, chat_id=call.message.chat.id, message_id=call.message.message_id)
    if not order:
        return None
    bot_model_user = BotModel.objects.get(user_id=order.user_id)
    change_status_get_manager_name = change_status_order(order=order, chat_id=call.message.chat.id, tag='in_progress')
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)
    manager_name = change_status_get_manager_name.get('manager_name')
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
        TEXT = f'Заказ номер: {order_number}'  # Не менять!!
        bot.send_message(call.message.chat.id, text=TEXT,
                         reply_markup=markup_managers)


@bot.callback_query_handler(func=lambda call: call.data == 'Взять в работу без запроса')
def take_order_manager(call):
    """Если менеджер взял заказ в работу, статус заказа меняется на in_progress"""
    text = call.message.text
    tag = 'номер:'
    order_id = get_order_from_text(text=text, tag=tag)
    if order_id is None or not str(order_id).isdigit():
        return bot.send_message(call.message.chat.id, text='id магазина должно быть числом и не None')
    order = check_status_order(order_id=order_id, chat_id=call.message.chat.id, message_id=call.message.message_id)
    if not order:
        return None
    change_status_order(order=order, chat_id=call.message.chat.id, tag='in_progress')
    empty_markup = InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=empty_markup)
    # bot.send_message(chat_id=bot_model_user.chat_id, text=f'Здравствуйте, {order.user.username}, я ваш менеджер меня '
    #                                                       f'зовут {manager_model_bot.user.username} скоро я с вами '
    #                                                       f'свяжусь для уточнения деталей заказа')

    return bot.send_message(call.message.chat.id, f'Вы взяли в работу заказ с номером {order_id}')


@bot.callback_query_handler(func=lambda call: call.data == 'заказы назначенные мне')
def get_orders_assigned_me(call):
    """Получение заказов закрепленных менеджером"""
    manager_model_bot = BotModel.objects.select_related('user').get(chat_id=call.message.chat.id)
    manager = AdministrativeStaffModel.objects.prefetch_related('order_in_work').get(
        baseusermodel_ptr_id=manager_model_bot.user.id)
    all_assigned_me_orders = manager.order_in_work.all()
    if not all_assigned_me_orders:
        return bot.send_message(call.message.chat.id, 'У вас нет активных заказов')
    for item in all_assigned_me_orders:
        order_number = item.id
        markup_managers = InlineKeyboardMarkup()
        but1 = InlineKeyboardButton('Отметить как выполненный', callback_data='Отметить как выполненный')
        markup_managers.row(but1)
        TEXT = f'Заказ номер: {order_number}'  # Не менять!!
        bot.send_message(call.message.chat.id, text=TEXT, reply_markup=markup_managers)


@bot.callback_query_handler(func=lambda call: call.data == 'Отметить как выполненный')
def change_order_status(call):
    """Изменение статуса заказа на выполнено"""
    text = call.message.text
    tag = 'номер:'
    order_id = get_order_from_text(text=text, tag=tag)
    if order_id is None or not str(order_id).isdigit():
        return bot.send_message(call.message.chat.id, text='id магазина должно быть числом и не None')
    if not order_id:
        return None
    order = Order.objects.get(id=order_id)
    change_status_order(order=order, chat_id=call.message.chat.id, tag='completed')
    bot.send_message(chat_id=call.message.chat.id, text=f'Вы завершили заказ {order_id}')


@bot.callback_query_handler(func=lambda call: call.data == 'адреса компании')
def get_post_address_store(call):
    """Получить или изменить адреса магазинов"""
    get_menu_address_store(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'Посмотреть адреса магазинов')
def show_address_store(call):
    """Получение адресов магазинов"""
    address_store = AddressArtFood.objects.prefetch_related('city', 'district').all()
    get_address_store(address_store=address_store, chat_id=call.message.chat.id, tag='look')


@bot.callback_query_handler(func=lambda call: call.data == 'Изменить адреса магазинов')
def change_store_address(call):
    """Изменить адрес магазина"""
    address_store = AddressArtFood.objects.prefetch_related('city', 'district').all()
    get_address_store(address_store=address_store, chat_id=call.message.chat.id, tag='change')


@bot.callback_query_handler(func=lambda call: call.data == 'Изменить адрес')
def change_one_address(call):
    text = call.message.text
    tag = 'id:'
    id_store = get_order_from_text(text=text, tag=tag)
    if id_store is None or not str(id_store).isdigit():
        return bot.send_message(call.message.chat.id, text='id магазина должно быть числом и не None')
    store = AddressArtFood.objects.get(id=id_store)
    bot.send_message(call.message.chat.id, 'Введите название улицы')
    bot.register_next_step_handler(call.message, change_street, store_id=store.id)


@bot.callback_query_handler(func=lambda call: call.data == 'редактор сообщений бота')
def get_message_bot(call):
    """Получение сообщений бота"""

    all_messages = BotMessage.objects.all()
    if not all_messages:
        return bot.send_message(call.message.chat.id, 'Нет сообщений для редактирования')

    for item in all_messages:

        if item.introductory_message:
            markup = button_change_message(callback_data='редактировать_1')
            type_message = 'вступительное сообщение'
            bot.send_message(call.message.chat.id, f'тип: {type_message}\n\n{item.introductory_message}',
                             reply_markup=markup)

        if item.message_after_hours:
            markup = button_change_message(callback_data='редактировать_2')
            type_message = 'сообщение в нерабочее время'
            bot.send_message(call.message.chat.id, f'тип: {type_message}\n\n{item.message_after_hours}',
                             reply_markup=markup)

        if item.message_order_not_site:
            markup = button_change_message(callback_data='редактировать_3')
            type_message = 'сообщение заказ не через сайт'
            bot.send_message(call.message.chat.id, f'тип: {type_message}\n\n{item.message_order_not_site}',
                             reply_markup=markup)

        if item.introductory_message_anonymous:
            markup = button_change_message(callback_data='редактировать_4')
            type_message = 'вступительное сообщение для не зарегистрированного пользователя'
            bot.send_message(call.message.chat.id, f'тип: {type_message}\n\n{item.introductory_message_anonymous}',
                             reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('редактировать_'))
def change_message_bot(call):
    """Изменение сообщений бота"""
    button_data = call.data.split('_')
    if not len(button_data) == 2:
        return
    type_message = button_data[1]
    if type_message == '1':
        bot.send_message(call.message.chat.id, 'Введите новое вступительное сообщение для зарегистрированного '
                                               'пользователя.\nВнимание! В начало сообщения автоматически подставляется'
                                               'имя пользователя')
        bot.register_next_step_handler(call.message, change_message, mess='introductory_message')

    if type_message == '2':
        bot.send_message(call.message.chat.id, 'Введите новое сообщение для обращения пользователя в не рабочее время')
        bot.register_next_step_handler(call.message, change_message, mess='message_after_hours')

    if type_message == '3':
        bot.send_message(call.message.chat.id, 'Введите новое сообщение если пользователь выбрал, что не заказывал '
                                               'товар через сайт')
        bot.register_next_step_handler(call.message, change_message, mess='message_order_not_site')

    if type_message == '4':
        bot.send_message(call.message.chat.id, 'Введите новое вступительное сообщение для не зарегистрированного '
                                               'пользователя\nВнимание! В месте с сообщением будет присылаться кнопка '
                                               'CANCEL для отмены подтверждения регистрации.')
        bot.register_next_step_handler(call.message, change_message, mess='introductory_message_anonymous')


@bot.callback_query_handler(func=lambda call: call.data == 'изменить время работы')
def get_opening_hours(call):
    """Получение всех магазинов и добавление кнопки изменить время работы"""
    all_store = AddressArtFood.objects.select_related('city').all()
    if not all_store:
        return bot.send_message(call.message.chat.id, 'Не зарегистрировано ни одного магазина')
    for item in all_store:
        store_id = str(item.id)
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton('изменить время работы', callback_data='get_opening_hours&' + store_id)
        markup.add(button)
        bot.send_message(call.message.chat.id, f'{item.city.name}, {item.street}, {item.house_number}',
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('get_opening_hours&'))
def change_opening_hours(call):
    """Выбор магазина и дня недели для изменения"""
    button_data = call.data.split('&')
    if not len(button_data) == 2:
        return
    store_id = button_data[1]

    bot.send_message(call.message.chat.id, 'Выберете день недели')
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    for i in days_of_week:
        markup = InlineKeyboardMarkup()
        callback_data = f'change_open_day&{i}&{store_id}'
        button = InlineKeyboardButton('выбрать', callback_data=callback_data)
        markup.add(button)
        bot.send_message(call.message.chat.id, text=i, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_open_day&'))
def change_opening_hours_day(call):
    """Создание нового режима работы магазина и выбор изменять: время открытия или время закрытия"""
    button_data = call.data.split('&')
    if not len(button_data) == 3:
        return
    week_day = button_data[1]
    store_id = button_data[2]
    store = AddressArtFood.objects.prefetch_related('open_store').get(id=store_id)
    open_store_day: OpenStore = store.open_store.filter(day__iexact=week_day).first()
    if not open_store_day:
        bot.send_message(call.message.chat.id, 'введите время открытия магазина в формате %H:%M:%S')
        bot.register_next_step_handler(call.message, get_new_open_hours, day=week_day, address=store)
    elif open_store_day:
        markup = InlineKeyboardMarkup()
        callback_data_open = f'change_hours_open&{week_day}&{store_id}'
        button_open = InlineKeyboardButton('время открытия', callback_data=callback_data_open + '&1')
        button_close = InlineKeyboardButton('время закрытия', callback_data=callback_data_open + '&2')
        markup.row(button_open, button_close)
        bot.send_message(call.message.chat.id, 'Выберите что требуется изменить', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_hours_open&'))
def change_hours_day(call):
    button_data = call.data.split('&')
    if not len(button_data) == 4:
        return
    store_id = button_data[2]
    week_day = button_data[1]
    tag = button_data[3]
    bot.send_message(call.message.chat.id, 'введите время открытия магазина в формате %H:%M:%S')
    bot.register_next_step_handler(call.message, change_open_hours_store, week_day=week_day, store_id=store_id,
                                   tag=tag)
