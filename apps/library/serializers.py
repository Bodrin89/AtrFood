from apps.library.models import City, Country, District, ManufacturingCompany, PackageType
from rest_framework import serializers


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
        model = Country
        fields = ['name', ]


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ['name', ]
