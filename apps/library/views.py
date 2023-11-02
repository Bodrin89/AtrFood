from dal import autocomplete
from rest_framework.generics import ListAPIView
from apps.library.models import PrivacyPolicy, ReturnPolicy, AboutCompany, City, District, AddressArtFood, SocialNetwork
from apps.library.serializers import ReturnPolicySerializer, PrivacyPolicySerializer, AboutCompanySerializer, \
    AddressArtFoodSerializer, SocialNetworkSerializer


class PrivacyPolicyView(ListAPIView):
    serializer_class = PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.all()


class ReturnPolicyView(ListAPIView):
    serializer_class = ReturnPolicySerializer
    queryset = ReturnPolicy.objects.all()


class AboutCompanyView(ListAPIView):
    serializer_class = AboutCompanySerializer
    queryset = AboutCompany.objects.all()


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


