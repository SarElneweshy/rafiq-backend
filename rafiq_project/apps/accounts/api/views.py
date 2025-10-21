from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import authenticate

class RegisterAPIView(APIView):
    permission_classes = []  # allow any
    authentication_classes = []
    
    # Validate and create a new user
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)# Generate auth token for the created user
        data = {
            "token": token.key,
            "user": UserSerializer(user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)
    

class LoginAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email') or request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    














# accounts/api/views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RequestPasswordResetSerializer, SetNewPasswordSerializer

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class RequestPasswordResetAPIView(APIView):
    permission_classes = []  

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"detail": "If that email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/accounts/reset-password/{uidb64}/{token}/"

        subject = "Password reset for your account"
        message = f"Click the link to reset your password: {reset_link}\nIf you didn't request this, ignore."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

        return Response({"detail": "If that email exists, a reset link has been sent."}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(APIView):
    permission_classes = []  

    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)

        if serializer.is_valid():
                serializer.save(uidb64=uidb64, token=token)
                return Response(
                    {"detail": "Password has been reset successfully."},
                    status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

