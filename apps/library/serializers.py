from apps.library.models import (
    City,
    CountryManufacturer,
    District,
    ManufacturingCompany,
    PackageType,
    ReturnPolicy,
    PrivacyPolicy,
    AboutCompany, AddressArtFood, OpenStore, ContactArtFood, SocialNetwork,
)
from rest_framework import serializers

from config.settings import LOGGER


class PackageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageType
        fields = ['name', ]


class ManufacturingCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = ManufacturingCompany
        fields = ['name', 'logo']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['name', ]


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = CountryManufacturer
        fields = ['name', ]


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ['name', ]


class ReturnPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReturnPolicy
        fields = ['name', ]


class PrivacyPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivacyPolicy
        fields = ['name', ]


class AboutCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutCompany
        fields = ['name', ]


class OpenStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenStore
        fields = ('day', 'time_open', 'time_close')

class ContactArtFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactArtFood
        fields = ('phone_numbers',)

class AddressArtFoodSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    district = DistrictSerializer()
    open_store = OpenStoreSerializer(many=True)
    contact_store = ContactArtFoodSerializer(many=True)

    class Meta:
        model = AddressArtFood
        fields = ('city', 'district', 'street', 'house_number', 'office_number', 'url', 'open_store', 'contact_store')

    def get_open_store(self, obj):
        """Получение значений из OpenStore"""
        open_store_instance = obj.open_store.all()
        open_store_serializer = OpenStoreSerializer(open_store_instance)
        return open_store_serializer.data

    def get_contact_art_food(self, obj):
        """Получение значений из ContactArtFood"""
        contact_store_instance = obj.contact_store.all()
        contact_store_serializer = ContactArtFoodSerializer(contact_store_instance)
        return contact_store_serializer


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('name', 'url_network')

