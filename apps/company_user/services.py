from django.contrib.auth.hashers import make_password

from apps.company_user.models import CompanyUserModel, ContactPersonModel
from apps.user.models import RegionModel, AddressModel


class CompanyUserServices:

    @staticmethod
    def create_company(validated_data: dict) -> CompanyUserModel:
        """Создание нового пользователя и сохранение его в БД с захэшированным паролем"""
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        contact_person_data = validated_data.pop('contact_person', None)
        address_data = validated_data.pop('address', None)
        contact_person = ContactPersonModel.objects.create(**contact_person_data)
        region_data = validated_data.pop('region', None)
        region = RegionModel.objects.create(**region_data)
        company_user = CompanyUserModel.objects.create(region=region, contact_person=contact_person, **validated_data)
        AddressModel.objects.create(user=company_user, **address_data)
        return company_user
