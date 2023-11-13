from datetime import datetime

import pytz
from django.core.cache import cache

from apps.library.models import AddressArtFood
from apps.tg_bot.models import BotMessage
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
