from rest_framework.generics import CreateAPIView

from apps.company_user.serializers import CreateCompanySerializer
from apps.user.models import AddressModel


class SingUpCompanyView(CreateAPIView):
    """Регистрация нового юридического пользователя"""
    serializer_class = CreateCompanySerializer
