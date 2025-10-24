from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from .models import DriverProfile
from .serializers import DriverProfileSerializer

#  Shared role-checking logic
def get_driver_queryset_for_user(user):
    if user.is_anonymous:
        return DriverProfile.objects.none()
    if user.role in ["admin", "client"]:
        return DriverProfile.objects.all()
    if user.role == "driver":
        return DriverProfile.objects.filter(user=user)
    return DriverProfile.objects.none()

# Django views
def driver_list_view(request):
    drivers = get_driver_queryset_for_user(request.user)
    return render(request, 'drivers/driver_list.html', {'drivers': drivers})

def driver_detail_view(request, pk):
    driver = get_object_or_404(DriverProfile, pk=pk)
    return render(request, 'drivers/driver_detail.html', {'driver': driver})

#  Custom permission
class IsAdminOrDriverSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.role == "admin" or
            (request.user.role == "driver" and obj.user == request.user)
        )

#  DRF ViewSet
class DriverProfileViewSet(viewsets.ModelViewSet):
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAdminOrDriverSelf]

    def get_queryset(self):
        return get_driver_queryset_for_user(self.request.user)
