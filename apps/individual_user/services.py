from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from apps.individual_user.models import IndividualUserModel
from apps.user.tasks import confirmation_email
from config.settings import LOGGER
from apps.clients.models import AddressModel


class IndividualUserService:

    @staticmethod
    def create_individual(request, validated_data: dict) -> IndividualUserModel:
        """Создание нового пользователя и сохранение его в БД с захэшированным паролем"""
        with transaction.atomic():
            del validated_data['password_repeat']
            validated_data['password'] = make_password(validated_data['password'])
            addresses_data = validated_data.pop('addresses', [])
            user = IndividualUserModel.objects.create(
                is_active=False,
                **validated_data
            )
            for address_data in addresses_data:
                AddressModel.objects.create(user=user, **address_data)
            message = _('Для подтверждения email, пожалуйста, перейдите по ссылке:')
            subject = _('Подтверждение email')
            email_url = 'api/user/confirm-email'
            confirmation_email.apply_async(args=[
                user.confirmation_token,
                user.email,
                email_url,
                message,
                subject
                ]
            )
        return user
