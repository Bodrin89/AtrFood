from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from apps.company_user.serializers import CreateCompanySerializer, CompanyAddressSerializer, GetCompanyAddressSerializer
from rest_framework.viewsets import ModelViewSet
from apps.company_user.models import CompanyAddress, CompanyUserModel


class SingUpCompanyView(CreateAPIView):
    """Регистрация нового юридического пользователя"""
    serializer_class = CreateCompanySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(
                {
                    'status': 'Success',
                    'message': _('Подтверждение отправлено на ваш электронный адрес.')
                },
                status=status.HTTP_201_CREATED
            )
        return response


class CompanyAddressViewSet(ModelViewSet):
    """Просмотр и создание нового юр. адреса пользователя отдельно"""

    serializer_class = CompanyAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompanyAddress.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return GetCompanyAddressSerializer
        return self.serializer_class


