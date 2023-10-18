from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.db import transaction

from apps.company_user.models import CompanyUserModel, ContactPersonModel, CompanyAddress
from apps.user.models import AddressModel, RegionModel
from config.settings import LOGGER
from apps.user.services import UserServices


class CompanyUserServices:

    @staticmethod
    def create_company(request, validated_data: dict) -> CompanyUserModel:
        """Создание нового пользователя и сохранение его в БД с захэшированным паролем"""
        with transaction.atomic():
            del validated_data['password_repeat']
            validated_data['password'] = make_password(validated_data['password'])
            LOGGER.debug(validated_data)
            bank = validated_data.pop('bank', None)
            bank_ = bank.replace(" ", "")
            contact_person_data = validated_data.pop('contact_person', None)
            company_address_data = validated_data.pop('company_address', None)
            addresses_data = validated_data.pop('addresses', [])
            contact_person = ContactPersonModel.objects.create(**contact_person_data)
            region_data = validated_data.pop('region', None)
            region, created = RegionModel.objects.get_or_create(**region_data)
            company_address, created = CompanyAddress.objects.get_or_create(**company_address_data)
            company_user = CompanyUserModel.objects.create(region=region, bank=bank_, company_address=company_address,
                                                           contact_person=contact_person,
                                                           is_active=False,
                                                           user_type='company',
                                                           **validated_data)
            # AddressModel.objects.create(user=company_user, **address_data)
            for address_data in addresses_data:
                AddressModel.objects.create(user=company_user, **address_data)
            message = 'Для подтверждения email, пожалуйста, перейдите по ссылке:'
            subject = 'Подтверждение email'
            email_url = 'confirm-email'
            UserServices.confirmation_email(
                user_token=company_user.confirmation_token,
                message=message,
                subject=subject,
                email_url=email_url,
                user_email=company_user.email
            )
            # login(request, company_user)
        return company_user
