from rest_framework import serializers
from apps.doctors.models import Doctor
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Doctor
        fields = [
            'id',
            'name',
            'sub_specialty',
            'city',
            'area',
            'address',
            'rating',
            'reviews_count',
            'price',
            'image_url',
            'vezeeta_url',
        ]