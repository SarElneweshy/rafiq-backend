from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from apps.doctors.models import Doctor
from .serializers import DoctorListSerializer, DoctorDetailSerializer
from .filters import DoctorFilter


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
    
    serializer_class = DoctorListSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter 
    ]

    filterset_class = DoctorFilter
    search_fields = ['name']
    ordering_fields = ['rating', 'price', 'reviews_count']
    ordering = ['-rating', '-reviews_count']

    ALLOWED_PARAMS = {'city', 'area', 'name', 'ordering','page', 'min_rating'}
    @property
    def allowed_ordering(self):
        return sorted(set(self.ordering_fields) | {
            f"-{field}" for field in self.ordering_fields
        })
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        # Check for unknown query parameters
        unknown_params = (set(request.query_params.keys()) - self.ALLOWED_PARAMS)
        if unknown_params:
             raise ValidationError({
                "detail": (
                    "Unknown query parameter(s): "
                    f"{', '.join(sorted(unknown_params))}"
                )
            })
        #  validate ordering parameter
        ordering_param = request.query_params.get('ordering')
        if ordering_param is not None:
            ordering_param = ordering_param.strip()
            if ordering_param == "":
                raise ValidationError({
                    'ordering': 'Ordering parameter cannot be empty.'
                })
            if ordering_param not in self.allowed_ordering:
                raise ValidationError({
                    'ordering': f'Invalid ordering parameter: {ordering_param}. Allowed values are: {", ".join(self.allowed_ordering)}'
                })

    def get_queryset(self):
        return Doctor.objects.filter(is_active=True)
       
        
 # Detail view with disclaimer added to the response
class DoctorDetailView(generics.RetrieveAPIView):
    serializer_class = DoctorDetailSerializer
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