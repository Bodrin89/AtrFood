from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.individual_user.models import IndividualUserModel
from apps.individual_user.services import IndividualUserService
from apps.user.serializers import AddressSerializer, RegionSerializer
from apps.user.services import UserServices
from config.settings import LOGGER


class CreateIndividualSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового физического пользователя"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    password_repeat = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'}, required=False)
    second_phone_number = serializers.CharField(max_length=50, required=False)
    region = RegionSerializer(required=True)
    address = AddressSerializer(write_only=True)

    class Meta:
        model = IndividualUserModel
        fields = ('id', 'username', 'email', 'phone_number', 'second_phone_number', 'address', 'region', 'password',
                  'password_repeat')

    def validate(self, attrs: dict) -> dict:
        return UserServices.validate(attrs)

    def create(self, validated_data: dict) -> IndividualUserModel:
        return IndividualUserService.create_individual(validated_data)

    # def update(self, instance, validated_data):
    #     LOGGER.debug(instance)
