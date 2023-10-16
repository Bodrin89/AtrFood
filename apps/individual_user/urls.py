from django.urls import path

from apps.individual_user.views import SingUpIndividualView


urlpatterns = [
    path('signup_individual', SingUpIndividualView.as_view(), name='signup-individual'),
]
