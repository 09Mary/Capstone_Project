from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    )

    role = models.CharField (max_length=20, choices=[('client', 'Client'), ('driver', 'Driver')] )
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
