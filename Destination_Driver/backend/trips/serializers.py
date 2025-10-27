from rest_framework import serializers
from .models import TripBooking

class TripBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripBooking
        fields =  '__all__'
        read_only_fields = ['client', 'status', 'driver', 'date_time']
