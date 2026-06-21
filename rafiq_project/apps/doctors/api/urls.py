from django.urls import path
from .views import (
    DoctorListView,
    DoctorDetailView,
    CityListView,
    AreaListView,
)

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    # same api endpoint with query params for filtering by city and area
    # /api/doctors/?city=Cairo
    # /api/doctors/?city=Cairo&area=Maadi  

   path('cities/', CityListView.as_view(), name='doctor-cities'),
    path('areas/', AreaListView.as_view(), name='doctor-areas'),

   # GET /api/doctors/areas/?city=Cairo

    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),

]