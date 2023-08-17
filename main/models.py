from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class LoginCode(models.Model):
    code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=12, validators=[
            RegexValidator(regex=r"^7[\d]{10}$", message="Invalid phone number")
        ],)
    expires_at = models.DateTimeField()
