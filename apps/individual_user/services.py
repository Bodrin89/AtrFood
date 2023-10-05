from django.contrib.auth.hashers import make_password

from apps.individual_user.models import IndividualUserModel
from apps.user.models import RegionModel
from config.settings import LOGGER


class IndividualUserService:

    @staticmethod
    def create_individual(validated_data: dict) -> IndividualUserModel:
        """Создание нового пользователя и сохранение его в БД с захэшированным паролем"""
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        region_data = validated_data.pop('region', None)
        region = RegionModel.objects.create(**region_data)
        user = IndividualUserModel.objects.create(region=region, **validated_data)
        return user
