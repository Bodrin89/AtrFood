from django.contrib.auth import login, logout
from django.db.models import QuerySet
from rest_framework import mixins, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from apps.company_user.models import CompanyUserModel
from apps.company_user.serializers import CreateCompanySerializer, GetUpdateCompanySerializer
from apps.individual_user.models import IndividualUserModel
from apps.individual_user.serializers import CreateIndividualSerializer, GetUpdateIndividualSerializer
from apps.user.models import AddressModel
from apps.user.serializers import AddressSerializer, LoginSerializer, RegionSerializer
from apps.user.services import UserServices


class LoginView(CreateAPIView):
    """Вход в учетную запись"""
    serializer_class = LoginSerializer
    permission_classes = [~ permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserServices.login_user(request, serializer)
        login(request=request, user=user)
        return Response(data={'id': user.pk, 'email': user.email}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Выход из учетной записи"""

    def post(self, request) -> Response:
        logout(request)
        return Response({'detail': 'Logged out successfully.'})


class ProfileViewSet(ReadOnlyModelViewSet):
    """Просмотр профиля пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'company':
            return QuerySet(model=CompanyUserModel).filter(id=user.id)
        return QuerySet(model=IndividualUserModel).filter(id=user.id)

    def get_serializer_class(self):
        user = self.request.user
        if user.user_type == 'company':
            return CreateCompanySerializer
        return CreateIndividualSerializer


class AddressViewSet(ModelViewSet):
    """Просмотр и создание нового адреса пользователя отдельно"""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AddressModel.objects.filter(user=self.request.user)


class ClientViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    """Просмотр профиля и изменение данных пользователя"""
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'company':
            return QuerySet(model=CompanyUserModel).filter(id=user.id)
        return QuerySet(model=IndividualUserModel).filter(id=user.id)

    def get_serializer_class(self):
        user = self.request.user
        if user.user_type == 'company':
            return GetUpdateCompanySerializer
        return GetUpdateIndividualSerializer
