from django.urls import path
from apps.library.views import PrivacyPolicyView, ReturnPolicyView, AboutCompanyView

urlpatterns = [
    path('privacy_policy', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('return_policy', ReturnPolicyView.as_view(), name='return_policy'),
    path('about_company', AboutCompanyView.as_view(), name='about_company'),
]