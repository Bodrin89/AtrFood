from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.user.models import AddressModel, BaseUserModel, RegionModel

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор для входа по username и email"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = BaseUserModel
        fields = ('id', 'email', 'password',)
        read_only_fields = ('id',)

    def validate(self, data):
        email = data.get('email')
        user = User.objects.filter(email=email).first()
        if user is not None and not user.is_active:
            raise serializers.ValidationError('Аккаунт необходимо подтвердить по электронной почте.')

        return data


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор региона"""


    class Meta:
        model = RegionModel
        fields = ('region', 'city')
        # read_only_fields = ('id',)


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор для создания адреса"""

    class Meta:
        model = AddressModel
        fields = ('id', 'district', 'street', 'house_number', 'apartment_number', 'floor')
        read_only_fields = ('id',)

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated and not self.instance:
            if AddressModel.objects.filter(user=user).count() >= 3 and request.method != 'PUT':
                raise serializers.ValidationError('Вы не можете добавить более трех адресов.')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
