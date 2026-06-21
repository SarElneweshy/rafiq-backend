from rest_framework import serializers
from apps.doctors.models import Doctor
class DoctorListSerializer(serializers.ModelSerializer):
    reviews_display = serializers.SerializerMethodField()

    class Meta:
        model  = Doctor
        fields = [
            'id',
            'name',
            'sub_specialty',
            'rating',
            'reviews_display',
            'image_url',
            'vezeeta_url',
        ]
    
    def get_reviews_display(self, obj):
        return f"{obj.reviews_count} review{'s' if obj.reviews_count != 1 else ''}"

class DoctorDetailSerializer(serializers.ModelSerializer):
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