from django.urls import path
from .views import SignupView, LoginView, PasswordResetRequest, PasswordResetConfirm

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup_page'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('password-reset-request/', PasswordResetRequest.as_view(), name='password_reset_request_page'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm_page'),

]