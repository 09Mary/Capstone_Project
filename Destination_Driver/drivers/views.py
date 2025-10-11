from rest_framework import viewsets, permissions
from .models import DriverProfile
from .serializers import DriverProfileSerializer

class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer



class IsAdminOrDriverSelf(permissions.BasePermission):
    """
    Admins = full access
    Drivers = can only update their own profile
    Clients = read-only
    """
    def has_object_permission(self, request, view, obj):
        # Read-only allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admins can do anything
        if request.user.role == "admin":
            return True

        # Drivers can update their own profile
        if request.user.role == "driver" and obj.user == request.user:
            return True

        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated


class DriverProfileViewSet(viewsets.ModelViewSet):
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAdminOrDriverSelf]

    def get_queryset(self):
        user = self.request.user

        # Admins and Clients can see all drivers
        if user.role in ["admin", "client"]:
            return DriverProfile.objects.all()

        # Drivers only see their own profile
        if user.role == "driver":
            return DriverProfile.objects.filter(user=user)

        return DriverProfile.objects.none()
