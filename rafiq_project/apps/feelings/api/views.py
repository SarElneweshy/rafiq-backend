from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .authentication import FeelingTokenAuthentication
from ..models import Feeling
from .serializers import FeelingSerializer


class FeelingApiView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FeelingSerializer
    authentication_classes = [FeelingTokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Feeling.objects.filter(user=self.request.user)