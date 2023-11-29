from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.company_user.models import CompanyAddress, CompanyUserModel, ContactPersonModel
from apps.company_user.services import CompanyUserServices
from apps.company_user.validators import bik_validator, bin_iin_validator, iban_validator
from apps.user.serializers import AddressSerializer, GetAddressSerializer
from apps.user.services import UserServices
from apps.library.serializers import CitySerializer, CountrySerializer, DistrictSerializer


class ContactPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactPersonModel
        fields = ('surname', 'first_name', 'second_name')


class CompanyAddressSerializer(serializers.ModelSerializer):

    street = serializers.CharField(required=True, max_length=250)

    class Meta:
        model = CompanyAddress
        fields = ('id', 'city', 'district', 'street', 'house_number', 'office_number')
        read_only_fields = ['id', ]


class GetCompanyAddressSerializer(serializers.ModelSerializer):

    city = CitySerializer()
    district = DistrictSerializer()

    class Meta:
        model = CompanyAddress
        fields = ('id', 'city', 'district', 'street', 'house_number', 'office_number')
        read_only_fields = ['id', ]


class CreateCompanySerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового юридического пользователя"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    password_repeat = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'}, required=False)
    bin_iin = serializers.IntegerField(validators=[bin_iin_validator])
    bik = serializers.IntegerField(validators=[bik_validator])
    bank = serializers.CharField(validators=[iban_validator])
    company_address = CompanyAddressSerializer(required=True)
    contact_person = ContactPersonSerializer()
    addresses = AddressSerializer(many=True, required=True)
    user_type = serializers.CharField(read_only=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = CompanyUserModel
        fields = ('id', 'username', 'last_name', 'second_name', 'email', 'phone_number', 'company_name', 'bin_iin',
                  'iik', 'bank', 'bik', 'company_address', 'payment_method', 'contact_person', 'addresses',
                  'password', 'password_repeat', 'user_type')

    def validate(self, attrs: dict) -> dict:
        return UserServices.validate(attrs)

    def create(self, validated_data: dict) -> CompanyUserModel:
        request = self.context.get('request')
        return CompanyUserServices.create_company(request, validated_data)


class GetUpdateCompanySerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и смены информации для юр. лица кроме(email, password)"""

    email = serializers.CharField(read_only=True)
    company_name = serializers.CharField(required=True)
    bin_iin = serializers.IntegerField(validators=[bin_iin_validator])
    bik = serializers.IntegerField(validators=[bik_validator])
    bank = serializers.CharField(validators=[iban_validator])
    company_address = GetCompanyAddressSerializer(read_only=True)
    contact_person = ContactPersonSerializer(required=True)
    addresses = GetAddressSerializer(many=True, read_only=True)
    user_type = serializers.CharField(read_only=True)

    class Meta:
        model = CompanyUserModel
        fields = ('id', 'username', 'last_name', 'second_name', 'email', 'phone_number', 'company_name',
                  'company_address', 'bin_iin', 'iik', 'bank', 'bik', 'payment_method', 'contact_person',
                  'addresses', 'user_type')

        read_only_fields = ('id',)

    def validate_addresses(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError(_('Необходимо предоставить хотя бы один адрес.'))
        if len(value) > 3:
            raise serializers.ValidationError(_('Можно добавить не более трех адресов.'))
        return value

    def update(self, instance, validated_data):
        request = self.context.get('request')
    #     region_data = validated_data.pop('region', None)
    #     addresses_data = validated_data.pop('addresses', None)
        contact_person = validated_data.pop('contact_person', None)
    #     company_address = validated_data.pop('company_address', None)
    #
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Обновляем вложенное поле contact_person, если оно предоставлено
        if contact_person is not None:
            contact_serializer = ContactPersonSerializer(instance.contact_person, data=contact_person, partial=True)
            if contact_serializer.is_valid(raise_exception=True):
                contact_serializer.save()
    #
    #     # Обновляем вложенное поле company_address, если оно предоставлено
    #     if company_address is not None:
    #         company_address_serializer = CompanyAddressSerializer(instance.company_address, data=company_address, partial=True)
    #         if company_address_serializer.is_valid(raise_exception=True):
    #             company_address_serializer.save()
    #
    #     # Обновляем вложенные поля addresses, если они предоставлены
    #     new_addresses = []
    #     for address_data in request.data.get('addresses'):
    #         address_id = address_data.pop('id', None)
    #         context = self.context
    #         if address_id:
    #             # Обновление адреса
    #             address = AddressModel.objects.filter(id=address_id).first()
    #             address_serializer = AddressSerializer(instance=address, data=address_data, partial=True, context=context)
    #         else:
    #             # Создание нового адреса
    #             address_serializer = AddressSerializer(data=address_data,  context=context)
    #
    #         if address_serializer.is_valid(raise_exception=True):
    #             new_address = address_serializer.save(user=instance)
    #             new_addresses.append(new_address)
    #
    #     # Удаляем адреса, которые больше не связаны с пользователем
    #     for address in instance.addresses.all():
    #         if address not in new_addresses:
    #             address.delete()
    #
    #     instance.addresses.set(new_addresses)
    #
        instance.save()
        return instance
