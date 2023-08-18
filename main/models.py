from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


User = get_user_model()


class LoginCode(models.Model):
    code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=12, validators=[
            RegexValidator(regex=r"^7[\d]{10}$", message="Invalid phone number")
        ])
    expires_at = models.DateTimeField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    invite_code = models.CharField(max_length=6, unique=True)
    invited_users = models.ManyToManyField(User)
    code_invited = models.CharField(max_length=6, null=True)