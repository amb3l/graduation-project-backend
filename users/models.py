from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def _create_user(
            self,
            email,
            password=None,
            **extra_fields,
    ):
        extra_fields.setdefault('is_active', True)

        values = [email, password]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))

        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError(f'The {field_name} value must be set')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(make_password(password))

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UserModel(AbstractUser, PermissionsMixin):
    username = None

    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    passport_photo = models.ForeignKey(
        to='passport_photos.PassportPhotoModel',
        on_delete=models.CASCADE,
        blank=True,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_passport_confirmed = models.BooleanField(default=False)

    last_login = models.DateTimeField(default=timezone.now())

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def update_last_login(self):
        self.last_login = timezone.now()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def set_passport_photo(self, passport_photo):
        if passport_photo:
            self.is_passport_confirmed = True

    @property
    def data_for_guest(self):
        return {
            'id': self.pk,
            'name': self.name,
            'email': self.email,
            'date_joined': self.date_joined,
            'last_login': self.last_login,
        }

    @property
    def data_for_me(self):
        return {
            'id': self.pk,
            'name': self.name,
            'email': self.email,
        }

    def __str__(self):
        return self.email
