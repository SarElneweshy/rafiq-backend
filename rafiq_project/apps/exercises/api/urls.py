from django.urls import path
from .views import DisorderListAPIView, DisorderDetailAPIView

urlpatterns = [
    path('', DisorderListAPIView.as_view(), name='disorder-list'),
    path('<int:pk>/', DisorderDetailAPIView.as_view(), name='disorder-detail'),
]
