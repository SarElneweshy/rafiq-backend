from rest_framework import generics
from apps.doctors.models import Doctor
from .serializers import DoctorListSerializer, DoctorDetailSerializer


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer


class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer
    lookup_field = 'id'
