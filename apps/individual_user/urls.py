from django.urls import path

from apps.individual_user.views import SingUpIndividualView, GetAllIndividualUserView

urlpatterns = [
    path('signup_individual', SingUpIndividualView.as_view(), name='signup-individual'),

    path('get_all_individual_user', GetAllIndividualUserView.as_view(), name='get-all-individual-user'),
]
