from typing import Callable

from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.request import Request

from apps.company_user.models import CompanyUserModel, ContactPersonModel
from apps.individual_user.models import IndividualUserModel
from apps.user.models import BaseUserModel
from config.settings import LOGGER


class UserServices:

    # @staticmethod
    # def signup_user(user_data: CreateUserSerializer) -> User:
    #     """Создание нового пользователя и сохранение его в БД с захэшированным паролем"""
    #     del user_data.validated_data['password_repeat']
    #     user_data.validated_data['password'] = make_password(user_data.validated_data['password'])
    #     user = User.objects.create(**user_data.validated_data)
    #     return user

    @staticmethod
    def validate(attrs: dict) -> dict:
        """Проверка введенного повторно пароля на валидность"""
        if not attrs.get('password_repeat', None):
            raise ValidationError('Required field')
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError('Password does not match')
        return attrs


    @staticmethod
    def login_user(user_data: Request, serializer_data: Callable) -> BaseUserModel:
        """Аутентификация пользователя"""

        if not (user := authenticate(
                password=user_data.data.get('password', None),
                email=user_data.data.get('email', None)
        )):
            raise AuthenticationFailed
        else:
            # serializer = serializer_data(data={'password': user.password, 'email': user.email})
            # # serializer.is_valid(raise_exception=True)
            return user

    @staticmethod
    def confirmation_email(user_token, user_email,  email_url, message, subject):
        domain = settings.ALLOWED_HOSTS[0]
        subject = subject
        message = f'{message} {domain}/{email_url}/?token={user_token}'
        send_mail(subject, message, EMAIL_HOST_USER, [user_email, ])

    @staticmethod
    def update_email(user_token,  email_url, message, subject, new_email):
        domain = settings.ALLOWED_HOSTS[0]
        subject = subject
        message = f'{message} {domain}/{email_url}/?token={user_token}&email={new_email}'
        send_mail(subject, message, EMAIL_HOST_USER, [new_email, ])
