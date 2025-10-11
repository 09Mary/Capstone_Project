
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TripBooking
from .serializers import TripBookingSerializer


class TripBookinViewSet(viewsets.ModelViewSet):
    queryset = TripBooking.objects.all()
    serializer_class = TripBookingSerializer


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

        if user.role == "admin":
            return TripBooking.objects.all()
        if user.role == "client":
            return TripBooking.objects.filter(client=user)
        if user.role == "driver":
            return TripBooking.objects.filter(driver__user=user)
        return TripBooking.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role == "client":
            serializer.save(client=self.request.user)
        else:
            raise permissions.PermissionDenied("Only clients can create trips.")

    # -------------------------
    # Custom Actions
    # -------------------------
    @action(detail=True, methods=["put"], url_path="accept")
    def accept_trip(self, request, pk=None):
        trip = self.get_object()
        if request.user.role == "driver":
            trip.status = "accepted"
            trip.save()
            return Response({"status": "Trip accepted"})
        return Response({"error": "Only drivers can accept trips"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["put"], url_path="cancel")
    def cancel_trip(self, request, pk=None):
        trip = self.get_object()
        user = request.user

        if user.role == "admin" or (user.role == "client" and trip.client == user) or (user.role == "driver" and trip.driver and trip.driver.user == user):
            trip.status = "cancelled"
            trip.save()
            return Response({"status": "Trip cancelled"})
        return Response({"error": "Not allowed to cancel this trip"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["put"], url_path="complete")
    def complete_trip(self, request, pk=None):
        trip = self.get_object()
        if request.user.role == "driver" and trip.driver and trip.driver.user == request.user:
            trip.status = "completed"
            trip.save()
            return Response({"status": "Trip completed"})
        return Response({"error": "Only assigned drivers can complete trips"}, status=status.HTTP_403_FORBIDDEN)