from django.urls import path
from .views import DeviceRegisterView

urlpatterns = [
    path('register-device/', DeviceRegisterView.as_view(), name='register-device'),
]
