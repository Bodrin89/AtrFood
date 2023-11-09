from datetime import datetime

import pytz

from config.settings import LOGGER


def is_within_time_range(start_time, end_time, tz):
    """Функция сравнения времени"""
    now = datetime.now(pytz.timezone(tz)).time()
    start = datetime.strptime(start_time, "%H:%M:%S").time()
    end = datetime.strptime(end_time, "%H:%M:%S").time()
    return start <= now <= end


def get_week_day():
    """Функция, которая получает текущий день недели"""
    current_time = datetime.now()
    day_of_week = current_time.weekday()
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    formatted_day_of_week = days_of_week[day_of_week]
    return formatted_day_of_week


def get_store_not_city_user(cities_store, title):
    """Функция, которая получает все адреса и режимы работы магазинов не в городе пользователя"""
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
