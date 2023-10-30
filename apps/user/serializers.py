from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from apps.user.models import BaseUserModel
from apps.clients.models import AddressModel
from apps.library.serializers import CitySerializer, CountrySerializer, DistrictSerializer

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор для входа по username и email"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    remember = serializers.BooleanField(default=False)

    class Meta:
        model = BaseUserModel
        fields = ('id', 'email', 'password', 'remember')
        read_only_fields = ('id',)

    def validate(self, data):
        email = data.get('email')
        user = User.objects.filter(email=email).first()
        if user is not None and not user.is_active:
            raise serializers.ValidationError(_('Аккаунт необходимо подтвердить по электронной почте.'))
        return data


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор для создания адреса"""

    class Meta:
        model = AddressModel
        fields = ('id', 'country', 'city', 'district', 'street', 'house_number', 'apartment_number', 'floor')
        read_only_fields = ['id', ]

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated and not self.instance:
            if AddressModel.objects.filter(user=user).count() >= 3 and request.method != 'PUT':
                raise serializers.ValidationError(_('Вы не можете добавить более трех адресов.'))
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class GetAddressSerializer(serializers.ModelSerializer):

    country = CountrySerializer()
    city = CountrySerializer()
    district = DistrictSerializer()

    class Meta:
        model = AddressModel
        fields = ('id', 'country', 'city', 'district', 'street', 'house_number', 'apartment_number', 'floor')
        read_only_fields = ['id', ]


class EmailSerializer(serializers.Serializer):
    """Сериализатор для смены email"""

    email = serializers.EmailField(required=True)


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для смены пароля"""

    new_password = serializers.CharField(
        validators=[validate_password],
        write_only=True,
        style={'input_type': 'password'}
    )
    repeat_password = serializers.CharField(
        validators=[validate_password],
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('new_password', 'repeat_password')

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        repeat_password = attrs.get('repeat_password')
        if new_password != repeat_password:
            raise serializers.ValidationError({'repeat_password': _('Пароли не совпадают')})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
