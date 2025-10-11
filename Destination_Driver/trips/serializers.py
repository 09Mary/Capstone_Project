from rest_framework import serializers
from .models import TripBooking

class TripBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripBooking
        fields = ['id', 'client', 'driver', 'vehicle', 'pickup_location', 'destination', 'date_time', 'status']
