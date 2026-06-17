from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from apps.doctors.models import Doctor
from .serializers import DoctorSerializer


# List view with filtering, searching, ordering, and disclaimer in the response


class DoctorListView(generics.ListAPIView):
    """
    GET /api/doctors/               
    GET /api/doctors/?city=Cairo           
    GET /api/doctors/?city=Cairo&area=Maadi 
    GET /api/doctors/?ordering=price      
    GET /api/doctors/?ordering=-rating     
    GET /api/doctors/?city=fayoum&search=ahmed        
    """
    
    serializer_class = DoctorSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter 
    ]

    filterset_fields = ['city', 'area']
    search_fields = ['name', 'sub_specialty', 'area']
    ordering_fields = ['rating', 'price', 'reviews_count']
    ordering = ['-rating', '-reviews_count']

    def get_queryset(self):
        return Doctor.objects.filter(is_active=True)

 # Detail view with disclaimer added to the response
class DoctorDetailView(generics.RetrieveAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.filter(is_active=True)


# View to list all cities with active doctors

class CityListView(APIView):
    def get(self, request):
        cities = (
            Doctor.objects
            .filter(is_active=True)
            .exclude(city='')
            .values_list('city', flat=True)
            .distinct()
            .order_by('city')
        )
        return Response({
            'count'  : cities.count(),
            'cities' : list(cities),
        })
# View to list areas in a specific city with active doctors

class AreaListView(APIView):
    def get(self, request):
        city = request.query_params.get('city', '').strip()
        if not city:
            raise ValidationError({
                'city': 'city parameter is required. Example: ?city=Cairo'
            })
        areas = (
            Doctor.objects
            .filter(is_active=True, city__iexact=city)
            .exclude(area='')
            .values_list('area', flat=True)
            .distinct()
            .order_by('area')
        )
        if not areas.exists():
            raise ValidationError({
                'city': f'No doctors found in city: {city}'
            })
        return Response({
            'city'  : city,
            'count' : areas.count(),
            'areas' : list(areas),
        })