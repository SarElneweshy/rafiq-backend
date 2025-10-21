from django.views.generic import TemplateView

class SignupView(TemplateView):
    template_name = "signup.html"

class LoginView(TemplateView):
    template_name = "login.html"

class PasswordResetRequest(TemplateView):
    template_name = "password_reset_request.html"

class PasswordResetConfirm(TemplateView):
    template_name = "password_reset_confirm.html"

