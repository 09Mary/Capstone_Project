from rest_framework import viewsets, permissions
from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Drivers only see their own vehicles
        if self.request.user.role == "driver":
            return Vehicle.objects.filter(driver__user=self.request.user)
        return Vehicle.objects.all()

    def perform_create(self, serializer):
        # Only drivers can add vehicles
        if self.request.user.role == "driver":
            serializer.save(driver=self.request.user.driver_profile)
        else:
            raise PermissionError("Only drivers can add vehicles.")
