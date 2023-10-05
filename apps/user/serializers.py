from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.user.models import IndividualUserModel, CompanyUserModel, BaseUserModel, ContactPersonModel
from apps.user.services import UserServices
from config.settings import LOGGER


class CreateIndividualSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового физического пользователя"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    password_repeat = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'}, required=False)
    second_phone_number = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = IndividualUserModel
        fields = ('id', 'username', 'email', 'phone_number', 'second_phone_number', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        return UserServices.validate(attrs)

    def create(self, validated_data: dict) -> IndividualUserModel:
        model = self.Meta.model
        return UserServices.create(model, validated_data)


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPersonModel
        fields = '__all__'


class CreateCompanySerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового юридического пользователя"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    password_repeat = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'}, required=False)
    contact_person = ContactPersonSerializer()

    class Meta:
        model = CompanyUserModel
        # exclude = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', )
        fields = ('id', 'username', 'email', 'phone_number', 'company_name', 'company_address', 'bin_iin', 'iik',
                  'bank', 'bik', 'payment_method', 'contact_person', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        return UserServices.validate(attrs)

    def create(self, validated_data: dict) -> CompanyUserModel:
        model = self.Meta.model
        return UserServices.create_company(model, validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор для входа по username и email"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = BaseUserModel
        fields = ('id', 'email', 'password')
        read_only_fields = ('id',)
