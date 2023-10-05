from django.contrib.auth import login
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


from apps.user.serializers import LoginSerializer
from apps.user.services import UserServices


class LoginView(CreateAPIView):
    """Вход в учетную запись"""
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer
        user = UserServices.login_user(request, serializer)
        login(request=request, user=user)
        return Response(data={'id': user.pk, 'username': user.username})

