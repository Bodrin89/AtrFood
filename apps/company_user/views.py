from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.company_user.serializers import CreateCompanySerializer
from apps.user.models import AddressModel


class SingUpCompanyView(CreateAPIView):
    """Регистрация нового юридического пользователя"""
    serializer_class = CreateCompanySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(
                {
                    'status': 'Success',
                    'message': 'Подтверждение отправлено на ваш электронный адрес.'
                },
                status=status.HTTP_201_CREATED
            )
        return response
