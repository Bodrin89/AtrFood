from typing import Callable

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.request import Request

from apps.user.models import BaseUserModel, IndividualUserModel, CompanyUserModel, ContactPersonModel
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
    def create(model, validated_data: dict) -> CompanyUserModel | IndividualUserModel:
        """Создание нового пользователя и сохранение его в БД с захэшированным паролем"""
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        user = model.objects.create(**validated_data)
        return user

    @staticmethod
    def create_company(model, validated_data: dict) -> CompanyUserModel | IndividualUserModel:
        """Создание нового пользователя и сохранение его в БД с захэшированным паролем"""
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        contact_person_data = validated_data.pop('contact_person', None)
        contact_person = ContactPersonModel.objects.create(**contact_person_data)
        LOGGER.debug(contact_person)
        company_user = CompanyUserModel.objects.create(contact_person=contact_person, **validated_data)
        return company_user

    @staticmethod
    def login_user(user_data: Request, serializer_data: Callable) -> BaseUserModel:
        """Аутентификация пользователя"""
        if not (user := authenticate(
                password=user_data.data.get('password', None),
                email=user_data.data.get('email', None)
        )):
            raise AuthenticationFailed
        else:
            serializer = serializer_data(data={'password': user.password, 'email': user.email})
            serializer.is_valid(raise_exception=True)
            return user
