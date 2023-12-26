from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from apps.individual_user.models import IndividualUserModel
from apps.individual_user.serializers import CreateIndividualSerializer, GetAllIndividualUserSerializer


class SingUpIndividualView(CreateAPIView):
    """Регистрация нового физического пользователя"""
    serializer_class = CreateIndividualSerializer

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



#TODO for 1C
class GetAllIndividualUserView(ListAPIView):
    permission_classes = permissions.IsAdminUser
    serializer_class = GetAllIndividualUserSerializer
    queryset = IndividualUserModel.objects.all()
