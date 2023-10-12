from django.urls import path

from apps.user.views import LoginView, LogoutView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
