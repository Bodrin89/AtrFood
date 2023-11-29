
def upload_to_folder_path(instance, filename, folder_name):
    """Создание пути для сохранения файла с товарами из подкатегории"""
    return f'documents/{folder_name}/{instance}/{filename}'
