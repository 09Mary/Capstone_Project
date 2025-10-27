from rest_framework import serializers
from .models import DriverProfile
from trips.models import TripBooking
from vehicles.models import Vehicle
from ratings.models import Rating


class TripBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripBooking
        fields = ['id', 'pickup_location', 'destination', 'status', 'date_time']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'plate_number', 'model', 'capacity']


class DriverProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # show username
    current_trips = serializers.SerializerMethodField()
    vehicle_info = serializers.SerializerMethodField()
    rating_summary = serializers.SerializerMethodField()  # ✅ added this

    class Meta:
        model = DriverProfile
        fields = [
            'id',
            'user',
            'license_number',
            'experience_years',
            'driver_type',
            'is_available',
            'current_trips',
            'vehicle_info',
            'rating_summary',
        ]

    def get_current_trips(self, obj):
        """Show all trips assigned to the driver"""
        trips = TripBooking.objects.filter(driver=obj)
        return TripBookingSerializer(trips, many=True).data

    def get_vehicle_info(self, obj):
        """Include vehicle if assigned"""
        vehicle = getattr(obj, 'vehicle', None)
        if vehicle:
            return VehicleSerializer(vehicle).data
        return None

    def get_rating_summary(self, obj):
        """Calculate average rating and total ratings for each driver."""
        trips = TripBooking.objects.filter(driver=obj, status="completed")
        ratings = Rating.objects.filter(trip__in=trips)

        if ratings.exists():
            avg_score = sum(r.score for r in ratings) / ratings.count()
            return {
                "average_score": round(avg_score, 1),
                "total_ratings": ratings.count()
            }
        return {
            "average_score": None,
            "total_ratings": 0
        }
