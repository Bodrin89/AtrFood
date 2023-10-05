from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.user.models import BaseUserModel, RegionModel, AddressModel


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор для входа по username и email"""
    password = serializers.CharField(validators=[validate_password],
                                     write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = BaseUserModel
        fields = ('id', 'email', 'password')
        read_only_fields = ('id',)


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegionModel
        fields = '__all__'
        read_only_fields = ('id',)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressModel
        fields = '__all__'
        read_only_fields = ('id', 'user')
