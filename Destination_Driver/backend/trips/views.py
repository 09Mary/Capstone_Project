from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TripBooking
from .serializers import TripBookingSerializer
from drivers.models import DriverProfile
import random


class TripPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == "admin":
            return True
        if user.role == "client" and obj.client == user:
            return True
        if user.role == "driver" and obj.driver and obj.driver.user == user:
            return True
        return False


class TripBookingViewSet(viewsets.ModelViewSet):
    serializer_class = TripBookingSerializer
    permission_classes = [TripPermission]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            return TripBooking.objects.filter(client=user)
        if user.role == "driver":
            return TripBooking.objects.filter(
                driver__user=user,
                status__in=["pending", "assigned","accepted"]
                )
        return TripBooking.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "client":
            raise PermissionDenied("Only clients can create trips.")

        # 🔹 Try to assign an available driver automatically
        available_drivers = DriverProfile.objects.filter(is_available=True)
        if not available_drivers.exists():
            raise PermissionDenied("No available drivers right now. Please try again later.")

        # Pick one randomly (later, you can improve this to choose nearest)
        assigned_driver = random.choice(list(available_drivers))

        # Create the trip and mark the driver unavailable
        trip = serializer.save(
            client=user,
            driver=assigned_driver, 
            status="assigned",
            pickup_location=self.request.data.get("pickup_location"),
            destination=self.request.data.get("destination")
            )
        assigned_driver.is_available = False
        assigned_driver.save()


    # --- CLIENT REQUESTS A SPECIFIC DRIVER ---
    @action(detail=False, methods=["post"], url_path="request_driver/(?P<driver_id>[^/.]+)")
    def request_driver(self, request, driver_id=None):
        user = request.user
        if user.role != "client":
            return Response({"error": "Only clients can request drivers."}, status=status.HTTP_403_FORBIDDEN)

        try:
            driver = DriverProfile.objects.get(id=driver_id, is_available=True)
        except DriverProfile.DoesNotExist:
            return Response({"error": "Driver not available or not found."}, status=status.HTTP_404_NOT_FOUND)

        trip = TripBooking.objects.create(
            client=user,
            driver=driver,
            pickup_location=request.data.get("pickup_location"),
            destination=request.data.get("destination"),
            status="pending"
        )

        driver.is_available = False
        driver.save()

        serializer = TripBookingSerializer(trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # --- DRIVER ACCEPTS A TRIP ---
    @action(detail=True, methods=["put"], url_path="accept")
    def accept_trip(self, request, pk=None):
        trip = self.get_object()
        if request.user.role == "driver" and trip.driver and trip.driver.user == request.user:
            trip.status = "accepted"
            trip.save()
            return Response({"status": "Trip accepted"})
        return Response({"error": "Only assigned drivers can accept trips"}, status=status.HTTP_403_FORBIDDEN)

    # --- DRIVER COMPLETES A TRIP ---
    @action(detail=True, methods=["put"], url_path="complete")
    def complete_trip(self, request, pk=None):
        trip = self.get_object()
        if request.user.role == "driver" and trip.driver and trip.driver.user == request.user:
            trip.status = "completed"
            trip.save()
            trip.driver.is_available = True
            trip.driver.save()
            return Response({"status": "Trip completed"})
        return Response({"error": "Only assigned drivers can complete trips"}, status=status.HTTP_403_FORBIDDEN)

    # --- CLIENT OR DRIVER CANCELS A TRIP ---
    @action(detail=True, methods=["put"], url_path="cancel")
    def cancel_trip(self, request, pk=None):
        trip = self.get_object()
        user = request.user

        if user.role == "admin" or (user.role == "client" and trip.client == user) or (user.role == "driver" and trip.driver and trip.driver.user == user):
            trip.status = "cancelled"
            trip.save()
            if trip.driver:
                trip.driver.is_available = True
                trip.driver.save()
            return Response({"status": "Trip cancelled"})

        return Response({"error": "Not allowed to cancel this trip"}, status=status.HTTP_403_FORBIDDEN)
