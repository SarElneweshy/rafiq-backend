from rest_framework import serializers
from apps.doctors.models import Doctor


class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'rating', 'reviews_count', 'image']


class DoctorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
