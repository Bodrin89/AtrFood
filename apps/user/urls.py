from django.urls import path

from apps.user.views import SingUpIndividualView, SingUpCompanyView, LoginView

urlpatterns = [
    path('signup_individual', SingUpIndividualView.as_view(), name='signup-individual'),
    path('signup_company', SingUpCompanyView.as_view(), name='signup-company'),
    path('login', LoginView.as_view(), name='login'),
]