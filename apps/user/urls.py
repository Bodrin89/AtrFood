from django.urls import path

from apps.user.views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
]