from django.db import models
from users.models import CustomUser 
from drivers.models import DriverProfile 
from vehicles.models import Vehicle 

class TripBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="trip_bookings")
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_assignments")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_vehicle")

    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Trip {self.id} - {self.client.username} → {self.destination}"
