from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rating
from .serializers import RatingSerializer
from trips.models import TripBooking


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        """Role-based permissions"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'add_rating']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Restrict ratings based on role"""
        user = self.request.user
        if user.role == "client":
            return Rating.objects.filter(client=user)
        elif user.role == "driver":
            return Rating.objects.filter(trip__driver__user=user)
        return Rating.objects.all()

    @action(detail=True, methods=['post'])
    def add_rating(self, request, pk=None):
        """Allow clients to rate a completed trip"""
        user = request.user
        try:
            trip = TripBooking.objects.get(pk=pk)
        except TripBooking.DoesNotExist:
            return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)

        # Only client who booked the trip can rate
        if trip.client != user:
            return Response({"error": "You can only rate your own trips."}, status=status.HTTP_403_FORBIDDEN)

        # Trip must be completed
        if trip.status != "completed":
            return Response({"error": "You can only rate completed trips."}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicate ratings
        if hasattr(trip, "rating"):
            return Response({"error": "This trip already has a rating."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=user, trip=trip)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)