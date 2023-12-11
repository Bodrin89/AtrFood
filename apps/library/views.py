from dal import autocomplete
from rest_framework.generics import ListAPIView
from apps.library.models import PrivacyPolicy, ReturnPolicy, AboutCompany, City, District, AddressArtFood, \
    SocialNetwork, CountryManufacturer, ManufacturingCompany
from apps.library.serializers import ReturnPolicySerializer, PrivacyPolicySerializer, AboutCompanySerializer, \
    AddressArtFoodSerializer, SocialNetworkSerializer, CitySerializer, DistrictSerializer, CountrySerializer, \
    ManufacturingCompanySerializer
from config.settings import LOGGER


class PrivacyPolicyView(ListAPIView):
    serializer_class = PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.all()


class ReturnPolicyView(ListAPIView):
    serializer_class = ReturnPolicySerializer
    queryset = ReturnPolicy.objects.all()


class AboutCompanyView(ListAPIView):
    serializer_class = AboutCompanySerializer
    queryset = AboutCompany.objects.all()


class CountryManufacturerView(ListAPIView):
    serializer_class = CountrySerializer
    queryset = CountryManufacturer.objects.all()


class ManufacturingCompanyView(ListAPIView):
    serializer_class = ManufacturingCompanySerializer
    pagination_class = None

    def get_queryset(self):
        query_params = self.request.query_params
        if subcategory := query_params.get('subcategory'):
            manufacture = ManufacturingCompany.objects.filter(
                product_data_manufacture__product__subcategory=subcategory
            ).prefetch_related('product_data_manufacture__product__subcategory')
            return set(manufacture)
        return ManufacturingCompany.objects.all()


class CityView(ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class DistrictView(ListAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class CityAutocomplete(autocomplete.Select2QuerySetView):
    """Для получения данных из формы с выбором города"""
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return City.objects.none()

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class DistrictAutocomplete(autocomplete.Select2QuerySetView):
    """Для получения данных из формы районов в зависимости от выбора города"""
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return District.objects.none()

        city_id = self.forwarded.get('city', None)
        qs = District.objects.filter(city_id=city_id)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class AddressArtFoodView(ListAPIView):
    """Получение всех адресов магазинов ArtFood"""
    queryset = AddressArtFood.objects.all()
    serializer_class = AddressArtFoodSerializer


class SocialNetworkView(ListAPIView):
    """Получение всех социальных сетей магазинов ArtFood"""
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworkSerializer





