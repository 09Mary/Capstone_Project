from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DriverProfile
from .serializers import DriverProfileSerializer
from trips.models import TripBooking
from ratings.models import Rating


# ---------- CUSTOM PERMISSION ----------
class IsAdminOrDriverSelf(permissions.BasePermission):
    """Only allow admins or the driver themselves to modify data."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == "admin"
            or (request.user.role == "driver" and obj.user == request.user)
        )


# ---------- MAIN DRIVER VIEWSET ----------
class DriverProfileViewSet(viewsets.ModelViewSet):
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAdminOrDriverSelf]

    def get_queryset(self):
        """Role-based access & rating filter."""
        user = self.request.user

        # --- Handle anonymous users safely ---
        if user.is_anonymous:
            return DriverProfile.objects.none()

        # --- Base queryset ---
        queryset = DriverProfile.objects.all()

        # --- Restrict drivers to their own profile ---
        if user.role == "driver":
            queryset = queryset.filter(user=user)

        # --- Optional: filter by minimum rating ---
        min_rating = self.request.query_params.get("min_rating")
        if min_rating:
            try:
                min_rating = float(min_rating)
                qualified_drivers = []
                for driver in queryset:
                    trips = TripBooking.objects.filter(driver=driver, status="completed")
                    ratings = Rating.objects.filter(trip__in=trips)
                    if ratings.exists():
                        avg_score = sum(r.score for r in ratings) / ratings.count()
                        if avg_score >= min_rating:
                            qualified_drivers.append(driver.id)
                queryset = queryset.filter(id__in=qualified_drivers)
            except ValueError:
                pass

        return queryset

    # ---------- LIST AVAILABLE DRIVERS ----------
    @action(detail=False, methods=["get"], url_path="available")
    def available_drivers(self, request):
        """List only available drivers."""
        available = DriverProfile.objects.filter(is_available=True)
        serializer = self.get_serializer(available, many=True)
        return Response(serializer.data)

    # ---------- DRIVER ACCEPTS TRIP ----------
    @action(detail=True, methods=["post"], url_path="accept_trip/(?P<trip_id>[^/.]+)")
    def accept_trip(self, request, pk=None, trip_id=None):
        """Allow a driver to accept a pending trip."""
        driver = self.get_object()
        try:
            trip = TripBooking.objects.get(id=trip_id)
        except TripBooking.DoesNotExist:
            return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)

        if trip.status != "pending":
            return Response({"error": "Trip is not available for acceptance."}, status=status.HTTP_400_BAD_REQUEST)

        trip.driver = driver
        trip.status = "accepted"
        trip.save()

        driver.is_available = False
        driver.save()

        return Response({"message": "Trip accepted successfully."}, status=status.HTTP_200_OK)

    # ---------- DRIVER COMPLETES TRIP ----------
    @action(detail=True, methods=["post"], url_path="complete_trip/(?P<trip_id>[^/.]+)")
    def complete_trip(self, request, pk=None, trip_id=None):
        """Allow driver to mark a trip as completed."""
        driver = self.get_object()
        try:
            trip = TripBooking.objects.get(id=trip_id, driver=driver)
        except TripBooking.DoesNotExist:
            return Response({"error": "Trip not found or not assigned to this driver."},
                            status=status.HTTP_404_NOT_FOUND)

        if trip.status != "accepted":
            return Response({"error": "Only accepted trips can be completed."},
                            status=status.HTTP_400_BAD_REQUEST)

        trip.status = "completed"
        trip.save()

        driver.is_available = True
        driver.save()

        return Response({"message": "Trip marked as completed."}, status=status.HTTP_200_OK)
