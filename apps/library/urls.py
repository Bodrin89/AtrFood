from django.urls import path
from apps.library.views import PrivacyPolicyView, ReturnPolicyView, AboutCompanyView, AddressArtFoodView, \
    SocialNetworkView, CityView, DistrictView, CountryManufacturerView, ManufacturingCompanyView, \
    PolicyPaymentDeliveryView

urlpatterns = [
    path('privacy_policy', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('return_policy', ReturnPolicyView.as_view(), name='return_policy'),
    path('payment_delivery_policy', PolicyPaymentDeliveryView.as_view(), name='payment_delivery_policy'),
    path('about_company', AboutCompanyView.as_view(), name='about_company'),
    path('list_address_store', AddressArtFoodView.as_view(), name='list_address_store'),
    path('list_social_network', SocialNetworkView.as_view(), name='list_social_network'),
    path('countries', CountryManufacturerView.as_view(), name='countries'),
    path('manufacture', ManufacturingCompanyView.as_view(), name='manufacture'),
    path('cities', CityView.as_view(), name='cities'),
    path('districts', DistrictView.as_view(), name='districts'),
]