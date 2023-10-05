
from rest_framework.generics import CreateAPIView

from apps.individual_user.serializers import CreateIndividualSerializer


class SingUpIndividualView(CreateAPIView):
    """Регистрация нового физического пользователя"""
    serializer_class = CreateIndividualSerializer
