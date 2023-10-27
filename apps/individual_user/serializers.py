from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.individual_user.models import IndividualUserModel
from apps.individual_user.services import IndividualUserService
from apps.user.models import AddressModel
from apps.user.serializers import AddressSerializer, RegionSerializer
from apps.user.services import UserServices
from config.settings import LOGGER


class CreateIndividualSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового физического пользователя"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    password_repeat = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'}, required=False)
    second_phone_number = serializers.CharField(max_length=50, required=False, allow_blank=True)
    region = RegionSerializer(required=True)
    # address = AddressSerializer(write_only=True)
    addresses = AddressSerializer(required=True)
    user_type = serializers.CharField(read_only=True)

    class Meta:
        model = IndividualUserModel
        fields = ('id', 'username', 'email', 'phone_number', 'second_phone_number', 'addresses', 'region', 'password',
                  'password_repeat', 'user_type')

    def validate(self, attrs: dict) -> dict:
        return UserServices.validate(attrs)

    def create(self, validated_data: dict) -> IndividualUserModel:
        request = self.context.get('request')
        return IndividualUserService.create_individual(request, validated_data)

    # def update(self, instance, validated_data):
    #     LOGGER.debug(instance)


class GetUpdateIndividualSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и смены информации для физ лиц кроме(email, password)"""

    email = serializers.CharField(read_only=True)
    second_phone_number = serializers.CharField(max_length=50, required=False, allow_blank=True)
    region = RegionSerializer(required=True)
    addresses = AddressSerializer(many=True, required=True)
    user_type = serializers.CharField(read_only=True)

    class Meta:
        model = IndividualUserModel
        fields = ('id', 'username', 'email', 'phone_number', 'second_phone_number', 'addresses', 'region', 'user_type')
        read_only_fields = ('id',)

    def validate_addresses(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError(_('Необходимо предоставить хотя бы один адрес.'))
        if len(value) > 3:
            raise serializers.ValidationError(_('Можно добавить не более трех адресов.'))
        return value

    def update(self, instance, validated_data):
        request = self.context.get('request')
        region_data = validated_data.pop('region', None)
        addresses_data = validated_data.pop('addresses', None)

        # Обновляем основные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Обновляем вложенное поле region, если оно предоставлено
        if region_data is not None:
            region_serializer = RegionSerializer(instance.region, data=region_data, partial=True)
            if region_serializer.is_valid(raise_exception=True):
                region_serializer.save()

        # Обновляем вложенные поля addresses, если они предоставлены
        new_addresses = []
        for address_data in request.data.get('addresses'):
            address_id = address_data.pop('id', None)
            context = self.context
            if address_id:
                # Обновление адреса
                address = AddressModel.objects.filter(id=address_id).first()
                address_serializer = AddressSerializer(instance=address, data=address_data, partial=True, context=context)
            else:
                # Создание нового адреса
                address_serializer = AddressSerializer(data=address_data,  context=context)

            if address_serializer.is_valid(raise_exception=True):
                new_address = address_serializer.save(user=instance)
                new_addresses.append(new_address)

        # Удаляем адреса, которые больше не связаны с пользователем
        for address in instance.addresses.all():
            if address not in new_addresses:
                address.delete()

        # Присваиваем новые адреса пользователю
        instance.addresses.set(new_addresses)

        instance.save()
        return instance
