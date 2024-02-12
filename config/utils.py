from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


UserModel = get_user_model()


class CaseInsensitiveUsernameModelBackend(ModelBackend):
    """
    Переопределяется метод класса аутентификации для того что бы при вводе email не учитывался регистр.
    При регистрации введенный email приводится в нижний регистр и при аутентификации приводится к нижнему
    """
    def authenticate(self, request, username=None, password=None, **kwargs):

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD).lower()
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user



def upload_to_folder_path(instance, filename, folder_name):
    """Создание пути для сохранения файла с товарами из подкатегории"""
    return f'documents/{folder_name}/{instance}/{filename}'

