
from rest_framework.generics import CreateAPIView

from apps.individual_user.serializers import CreateIndividualSerializer
from apps.user.models import BaseUserModel
from config.settings import LOGGER


class SingUpIndividualView(CreateAPIView):
    """Регистрация нового физического пользователя"""
    serializer_class = CreateIndividualSerializer

    def get_queryset(self):
        return BaseUserModel.objects.all()

