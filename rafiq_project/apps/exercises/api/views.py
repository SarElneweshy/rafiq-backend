from rest_framework import generics
from apps.exercises.models import Disorder
from .serializers import (
    DisorderListSerializer,
    DisorderDetailSerializer
)

class DisorderListAPIView(generics.ListAPIView):
    queryset = Disorder.objects.all()
    serializer_class = DisorderListSerializer


class DisorderDetailAPIView(generics.RetrieveAPIView):
    queryset = Disorder.objects.all()
    serializer_class = DisorderDetailSerializer
