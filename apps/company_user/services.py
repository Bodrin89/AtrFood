from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from apps.company_user.models import CompanyAddress, CompanyUserModel, ContactPersonModel
from apps.user.tasks import confirmation_email
from config.settings import LOGGER
from apps.clients.models import AddressModel


class CompanyUserServices:

    @staticmethod
    def create_company(request, validated_data: dict) -> CompanyUserModel:
        """Создание нового пользователя и сохранение его в БД с захэшированным паролем"""
        with transaction.atomic():
            del validated_data['password_repeat']
            validated_data['password'] = make_password(validated_data['password'])
            bank = validated_data.pop('bank', None)
            bank_ = bank.replace(' ', '')
            contact_person_data = validated_data.pop('contact_person', None)
            company_address_data = validated_data.pop('company_address', None)
            addresses_data = validated_data.pop('addresses', [])
            company_user = CompanyUserModel.objects.create(bank=bank_,
                                                           # is_active=False,
                                                           **validated_data)
            ContactPersonModel.objects.create(user=company_user, **contact_person_data)
            CompanyAddress.objects.create(user=company_user, **company_address_data)
            for address_data in addresses_data:
                AddressModel.objects.create(user=company_user, **address_data)
            message = _('Для подтверждения email, пожалуйста, перейдите по ссылке:')
            subject = _('Подтверждение email')
            email_url = 'api/user/confirm-email'
            # confirmation_email.apply_async(args=[
            #     company_user.confirmation_token,
            #     company_user.email,
            #     email_url,
            #     message,
            #     subject
            #     ]
            # )
            return company_user
