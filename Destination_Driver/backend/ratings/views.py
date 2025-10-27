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
        """Role-based permissions."""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'add_rating']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Role-based filtering of ratings."""
        user = self.request.user

        if not user.is_authenticated:
            return Rating.objects.none()

        if hasattr(user, "role"):  # Ensure 'role' exists on CustomUser
            if user.role == "client":
                return Rating.objects.filter(client=user)
            elif user.role == "driver":
                return Rating.objects.filter(trip__driver__user=user)
            elif user.role == "admin":
                return Rating.objects.all()

        return Rating.objects.none()

    @action(detail=False, methods=['post'])
    def add_rating(self, request):
        trip_id = request.data.get('trip_id')
        score = request.data.get('score')
        comment = request.data.get('comment', '')

        try:
            trip = TripBooking.objects.get(id=trip_id)
        except TripBooking.DoesNotExist:
            return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)

        # Assuming request.user is authenticated
        client = request.user
        if trip.client != client:
            return Response({"error": "You can only rate your own trips"}, status=status.HTTP_403_FORBIDDEN)

        if trip.status != "completed":
            return Response({"error": "You can only rate completed trips"}, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(trip, 'rating'):
            return Response({"error": "Trip already rated"}, status=status.HTTP_400_BAD_REQUEST)

        rating = Rating.objects.create(trip=trip, client=client, score=score, comment=comment)
        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)