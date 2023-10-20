from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.views import (AddressViewSet,
                             ClientViewSet,
                             ConfirmEmailView,
                             EmailUrlView,
                             ForgotPasswordView,
                             LoginView,
                             LogoutView,
                             ProfileViewSet,
                             UpdateEmailView,
                             UpdatePasswordViewInProfile,
                             UpdatePasswordViewNotInProfile,)

router = DefaultRouter()

router.register(r'profile', ClientViewSet, basename='profile')
router.register(r'full_profile_info', ProfileViewSet, basename='full_profile_info')
router.register(r'address', AddressViewSet, basename='address')

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('email_url', EmailUrlView.as_view(), name='email_url'),
    path('update-email/', UpdateEmailView.as_view(), name='update_email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('update-password/', UpdatePasswordViewNotInProfile.as_view(), name='update_password'),
    path('update-password_in_profile/', UpdatePasswordViewInProfile.as_view(), name='update_password_in_profile'),
] + router.urls
