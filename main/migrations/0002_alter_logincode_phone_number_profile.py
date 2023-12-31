# Generated by Django 4.2.4 on 2023-08-17 19:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logincode",
            name="phone_number",
            field=models.CharField(
                max_length=12,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Invalid phone number", regex="^7[\\d]{10}$"
                    )
                ],
            ),
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("invite_code", models.CharField(max_length=6, unique=True)),
                ("invited", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
