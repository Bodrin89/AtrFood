from django.urls import path

from apps.company_user.views import SingUpCompanyView

urlpatterns = [
    path('signup_company', SingUpCompanyView.as_view(), name='signup-company'),
]
