from django.urls import path
from apps.company_user.views import SingUpCompanyView, CompanyAddressViewSet, GetAllCompanyUserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'address_company', CompanyAddressViewSet, basename='address_company')

urlpatterns = [
    path('signup_company', SingUpCompanyView.as_view(), name='signup-company'),

    path('get_all_companyuser', GetAllCompanyUserView.as_view(), name='get-all-companyuser'),

] + router.urls

