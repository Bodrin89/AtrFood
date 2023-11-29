from django.contrib.auth import get_user_model, login, logout
from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from django.utils.translation import gettext_lazy as _
from apps.company_user.models import CompanyUserModel
from apps.company_user.serializers import CreateCompanySerializer, GetUpdateCompanySerializer
from apps.individual_user.models import IndividualUserModel
from apps.individual_user.serializers import CreateIndividualSerializer, GetUpdateIndividualSerializer
from apps.clients.models import AddressModel
from apps.user.serializers import (AddressSerializer,
                                   ChangePasswordSerializer,
                                   EmailSerializer,
                                   LoginSerializer,
                                   GetAddressSerializer,
                                   )
from apps.user.services import UserServices
from apps.user.tasks import confirmation_email, update_email

User = get_user_model()


class LoginView(CreateAPIView):
    """Вход в учетную запись"""

    serializer_class = LoginSerializer
    permission_classes = [~ permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            },
            example={
                'id': 1,
                'email': 'example@example.com',
            },
        )},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserServices.login_user(request, serializer)
        if request.data.get('remember') is None or request.data.get('remember') is False:
            request.session.set_expiry(0)
            request.session.modify = True
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

    def get_serializer_class(self):
        if self.action == 'list':
            return GetAddressSerializer
        return self.serializer_class


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


class ConfirmEmailView(APIView):
    """Подтверждение электронной почты при создании нового пользователя"""

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        user = get_user_model().objects.filter(confirmation_token=token).first()
        if user:
            user.is_active = True
            user.save()
            return Response(
                {
                    'status': 'Success',
                    'message': _('Email успешно подтвержден.')
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'status': 'Error',
                'message': _('Пользователь не найден.')
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class EmailUrlView(APIView):
    """Отправка подтверждения для смены электронной почты"""

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            if email == request.user.email:
                return Response(
                    {
                        'status': 'Error',
                        'message': _('У вас уже указана данная почта.')
                    },
                    status=status.HTTP_200_OK
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    {
                        'status': 'Error',
                        'message': _('Данная электронная почта уже зарегистрирована.')
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = self.request.user.confirmation_token
            message = _('Для подтверждения email, пожалуйста, перейдите по ссылке:')
            subject = _('Подтверждение email')
            email_url = 'api/user/update-email'
            update_email.apply_async(args=[
                token,
                email_url,
                message,
                subject,
                email
            ]
            )
            return Response(
                {
                    'status': 'Success',
                    'message': _(f'Уведомление отправлено на новую электронную почту:') + f'{email}'
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEmailView(APIView):
    """Смена Электронной почты"""

    def get(self, request):
        token = request.query_params.get('token')
        email = request.query_params.get('email')
        if not token or not email:
            return Response(
                {
                    'status': 'Error',
                    'message': _('Токен и email обязательны.')
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_user_model().objects.filter(confirmation_token=token).first()
        if user:
            user.email = email
            user.save()
            return Response(
                {
                    'status': 'Success',
                    'message': _('Email успешно изменен.')
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'status': 'Error',
                'message': _('Неверный токен или email.')
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class ForgotPasswordView(APIView):
    """Отправка подтверждения для восстановления пароля"""

    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = user.confirmation_token
                message = _('Для восстановления пароля перейдите по ссылке: ')
                subject = _('Восстановление пароля')
                email_url = 'api/user/update-password'
                confirmation_email.apply_async(args=[
                    token,
                    email,
                    email_url,
                    message,
                    subject,
                ]
                )
                return Response(
                    {
                        'status': 'Success',
                        'message': _(f'Уведомление отправлено на электронную почту:') + f'{email}'
                    },
                    status=status.HTTP_200_OK
                )

        return Response(
            {
                'status': 'Error',
                'message': _('Пользователь с данной электронной почтой не найден')
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class UpdatePasswordViewNotInProfile(APIView):
    """Воссстановление пароля"""

    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if not token:
            return Response(
                {
                    'status': 'Error',
                    'message': _('Неверная ссылка.')
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(confirmation_token=token).first()
        if not user:
            return Response(
                {
                    'status': 'Error',
                    'message': _('Пользователь не найден.')
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response(
                {
                    'status': 'Success',
                    'message': _('Пароль изменен.')
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordViewInProfile(APIView):
    """Смена пароля """

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            login(request, user)
            return Response(
                {
                    'status': 'Success',
                    'message': _('Пароль изменен.')
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
