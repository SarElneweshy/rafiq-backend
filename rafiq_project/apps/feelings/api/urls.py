from rest_framework.routers import DefaultRouter
from .views import FeelingApiView
from django.urls import path, include

router = DefaultRouter()
router.register("", FeelingApiView, basename="feeling")

urlpatterns = [
    path("", include(router.urls))
]