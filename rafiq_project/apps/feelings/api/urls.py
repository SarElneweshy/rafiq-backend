from rest_framework.routers import DefaultRouter
from .views import FeelingApiView
from django.urls import path, include

router = DefaultRouter()
router.register(r"feelings", FeelingApiView, basename="feeling")

urlpatterns = [
    path("", include(router.urls))
]