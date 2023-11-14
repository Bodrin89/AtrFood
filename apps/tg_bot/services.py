import json
import re
from datetime import datetime

import pytz
from django.core.cache import cache
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardMarkup, KeyboardButton

from apps.administrative_staff.models import AdministrativeStaffModel
from apps.library.models import AddressArtFood
from apps.order.models import Order
from apps.tg_bot import bot
from apps.tg_bot.models import BotMessage, BotModel
from apps.user.models import BaseUserModel
from config.settings import LOGGER, DEFAULT_MASSAGE_BOT, TIME_CACHE_TG_BOT_MESSAGE


def is_within_time_range(start_time, end_time, tz):
    """Функция сравнения времени"""
    now = datetime.now(pytz.timezone(tz)).time()
    start = datetime.strptime(start_time, "%H:%M:%S").time()
    end = datetime.strptime(end_time, "%H:%M:%S").time()
    return start <= now <= end


def get_week_day():
    """Функция получает текущий день недели"""
    current_time = datetime.now()
    day_of_week = current_time.weekday()
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    formatted_day_of_week = days_of_week[day_of_week]
    return formatted_day_of_week


def check_open_store(user, formatted_day_of_week):
    """Функция проверяет открыт ли магазин в данное время"""
    user_addresses = user.addresses.all()
    if user_addresses:
        cities_user = [item.city.name for item in user_addresses]
        cities_store = AddressArtFood.objects.filter(city__name__in=cities_user).prefetch_related('open_store').first()

        timezone = cities_store.city.timezone
        open_store = cities_store.open_store.all()
        res = {i.day: {'open': i.time_open.strftime("%H:%M:%S"), 'close': i.time_close.strftime("%H:%M:%S")} for i in
               open_store}
        work_time = res.get(formatted_day_of_week, {})
        return {'work_time': work_time, 'timezone': timezone}


def get_store_not_city_user(cities_store, title):
    """Функция получает все адреса и режимы работы магазинов не в городе пользователя"""
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

    response_text = f"<u>{title}</u>\n"

    for city, stores in store_open_store.items():
        response_text += f"\n<b>{city}</b>\n"
        for store_info in stores:
            response_text += "\n".join([f"{store_detail}: {value}" for store_detail, value in store_info.items()])
            response_text += "\n\n"
    return response_text


def get_bot_message_cache(cached_key):
    """Получение сообщения из кэша, БД или дефолтное"""
    if not (cached_value := cache.get(cached_key)):
        if bot_mes_obj := BotMessage.objects.first():
            value = getattr(bot_mes_obj, cached_key, None)
            cached_value = value or DEFAULT_MASSAGE_BOT[cached_key]
            cache.set(cached_key, cached_value, TIME_CACHE_TG_BOT_MESSAGE)
        else:
            cached_value = DEFAULT_MASSAGE_BOT[cached_key]
            cache.set(cached_key, cached_value, TIME_CACHE_TG_BOT_MESSAGE)
    return cached_value


def show_manager_menu(message: Message) -> None:
    """Меню менеджеров"""
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('редактор сообщений бота', callback_data='редактор сообщений бота')
    but2 = InlineKeyboardButton('адреса компании', callback_data='адреса компании')
    but3 = InlineKeyboardButton('изменить время работы', callback_data='изменить время работы')
    but4 = InlineKeyboardButton('заявки от клиентов', callback_data='заявки от клиентов')
    markup.add(but1)
    markup.add(but2)
    markup.add(but3)
    markup.add(but4)
    return bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


def get_menu(message):
    """Кнопка Меню для вывода основного меню"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = KeyboardButton('Меню')
    markup.add(but1)
    bot.send_message(message.chat.id, 'Меню',  reply_markup=markup)


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
            but1 = InlineKeyboardButton('Взять в работу', callback_data='Взять в работу')
            but2 = InlineKeyboardButton('Отказаться', callback_data='Отказаться')
            markup_managers.row(but1, but2)
            bot.send_message(chat_id=chat_id, text=f'Обработайте заказ номер: {order_number}',
                             reply_markup=markup_managers)
        except ApiTelegramException as e:
            """Обработка ошибки если номер заказа слишком большой и его не возможно передать в callback_data"""
            LOGGER.error(f'{e}, order_number: {but1_data.get("o")}')
    bot.send_message(message.chat.id, text=f'Ваш заказ обрабатывается')
    show_main_menu(message)


def get_order_from_text(text):
    """Получение номера заказа из сообщения"""
    match = re.search(r'номер: (\d+)', text)
    if match:
        order_number = match.group(1)
        return order_number


def check_status_order(order_id, chat_id, message_id):
    """Проверка статуса заказа"""
    order = Order.objects.select_related('user').get(id=order_id)
    if order.status not in ['new_paid', 'new_unpaid']:
        empty_markup = InlineKeyboardMarkup()
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=empty_markup)
        bot.send_message(chat_id, text='Заказ взят в работу другим менеджером')
        return None
    return order


def change_status_order(order, chat_id, order_id):
    """Изменение статуса после того как менеджер взял его в работу"""
    manager_model_bot = BotModel.objects.select_related('user').get(chat_id=chat_id)
    manager = AdministrativeStaffModel.objects.get(baseusermodel_ptr_id=manager_model_bot.user.id)
    manager.order_in_work_id = order_id
    order.status = 'in_progress'
    manager.save()
    order.save()
    return {'manager_name': manager_model_bot.user.username}
