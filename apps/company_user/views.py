from rest_framework.generics import CreateAPIView

from apps.company_user.serializers import CreateCompanySerializer


class SingUpCompanyView(CreateAPIView):
    """Регистрация нового юридического пользователя"""
    serializer_class = CreateCompanySerializer
