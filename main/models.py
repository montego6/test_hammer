from django.db import models

# Create your models here.

class LoginCode(models.Model):
    code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=12)
    expires_at = models.DateTimeField()
