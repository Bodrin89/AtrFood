from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.company_user.models import CompanyUserModel, ContactPersonModel
from apps.company_user.services import CompanyUserServices
from apps.user.serializers import AddressSerializer, RegionSerializer
from apps.user.services import UserServices


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPersonModel
        fields = ('surname', 'first_name', 'second_name')


class CreateCompanySerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового юридического пользователя"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    password_repeat = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'}, required=False)
    contact_person = ContactPersonSerializer()
    address = AddressSerializer(write_only=True)
    region = RegionSerializer()

    class Meta:
        model = CompanyUserModel
        fields = ('id', 'username', 'email', 'phone_number', 'company_name', 'company_address', 'bin_iin', 'iik',
                  'bank', 'bik', 'payment_method', 'contact_person', 'address', 'region', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        return UserServices.validate(attrs)

    def create(self, validated_data: dict) -> CompanyUserModel:
        return CompanyUserServices.create_company(validated_data)
