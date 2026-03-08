from rest_framework import generics, permissions
from ..models import Device
from .serializers import DeviceSerializer

class DeviceRegisterView(generics.CreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        Device.objects.update_or_create(
            user=self.request.user,
            defaults={'fcm_token': self.request.data.get('fcm_token')}
        )
