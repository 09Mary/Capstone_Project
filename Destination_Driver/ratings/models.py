from django.db import models
from users.models import CustomUser # type: ignore
from trips.models import TripBooking # type: ignore

class Rating(models.Model):
    trip = models.OneToOneField(TripBooking, on_delete=models.CASCADE, related_name="rating")
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ratings")
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.score} by {self.client.username} for Trip {self.trip.id}"
