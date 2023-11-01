from apps.library.models import (
    City,
    CountryManufacturer,
    District,
    ManufacturingCompany,
    PackageType,
    ReturnPolicy,
    PrivacyPolicy,
    AboutCompany,
)
from rest_framework import serializers


class PackageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageType
        fields = ['name', ]


class ManufacturingCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = ManufacturingCompany
        fields = ['name', ]


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