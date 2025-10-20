from django.db import models
from django.conf import settings

class DriverProfile(models.Model):
    DRIVER_TYPE_CHOICES = (
        ('with_vehicle', 'With Vehicle'),
        ('without_vehicle', 'Without Vehicle'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_profile"
    )
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.PositiveIntegerField(default=0)
    driver_type = models.CharField(max_length=20, choices=DRIVER_TYPE_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.driver_type}"
