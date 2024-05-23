from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

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


class UserModel(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
