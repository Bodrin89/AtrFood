from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.views import AddressViewSet, ClientViewSet, LoginView, LogoutView, ProfileViewSet

router = DefaultRouter()

router.register(r'profile', ClientViewSet, basename='profile')
router.register(r'full_profile_info', ProfileViewSet, basename='full_profile_info')
router.register(r'address', AddressViewSet, basename='address')

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
] + router.urls
