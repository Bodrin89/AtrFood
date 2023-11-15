import re


def validate_time_format(text):
    """Проверка времени на соответствие формату %H:%M:%S"""
    time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$')

    if time_pattern.match(text):
        return True
    else:
        return False


def validate_content_type(text):
    """Проверка является ли сообщение текстом"""
    if text == 'text':
        return True
    else:
        return False
