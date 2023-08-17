from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    phone_number = models.CharField(max_length=12,
        validators=[
            RegexValidator(regex=r"^7[\d]{10}$", message="Invalid phone number")
        ],
        unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.phone_number
