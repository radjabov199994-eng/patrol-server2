from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        OFFICER = "OFFICER", "Officer"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OFFICER)

    position = models.CharField(max_length=120, blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")

    photo = models.ImageField(upload_to="officers/", blank=True, null=True)  

    def __str__(self):
        return f"{self.username} ({self.role})"
