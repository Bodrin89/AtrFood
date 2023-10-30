import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.user.validators import validate_phone_number


class CustomUserManager(BaseUserManager):
    """Переопрделяем метод базового менеджера, чтобы поле username перестало быть required"""
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUserModel(AbstractUser):
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    USER_TYPES = (
        ('individual', _('Individual')),
        ('company', _('Company')),
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
        blank=True,
        null=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    last_name = None
    first_name = None
    phone_number = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        verbose_name=_('номер телефона')
        )
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='individual', verbose_name=_('Тип пользователя'))
    email = models.EmailField(unique=True, verbose_name=_('Электронная почта'))

    objects = CustomUserManager()

    # def get_absolute_url(self):
    #     return reverse('')


