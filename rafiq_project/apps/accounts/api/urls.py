from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterAPIView, LoginAPIView, RequestPasswordResetAPIView, SetNewPasswordAPIView

urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='api-signup'),
    path('login/', LoginAPIView.as_view(), name='api-login'),  # returns {"token": "..."}
    path('password-reset/', RequestPasswordResetAPIView.as_view(), name='api-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', SetNewPasswordAPIView.as_view(), name='api-password-reset-confirm'),
]