from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

# This serializer is used to return user information after authentication (e.g., sign-in) by
# from rest_framework.authtoken.views import obtain_auth_token .
# We intentionally exclude the password field for security reasons — passwords should never
# be exposed in API responses. Only non-sensitive user details are serialized here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name')


class RegisterSerializer(serializers.ModelSerializer):
    # Password field (write-only): accepts the raw password on input, enforces a minimum length,
    # and is used to set the user's hashed password. It will NOT be returned in API responses.
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email','first_name','last_name','password')
    
    # Validate that the provided email is unique (case-insensitive).
    # If a user with the same email already exists, raise a validation error.
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    # Custom create method for handling user registration.
    # - Receives validated_data from the serializer after validation.
    # - Extracts the raw password separately (using pop) to prevent it from being saved as plain text.
    # - Calls create_user(), which automatically hashes the password and creates the user instance.
    # - Returns the newly created user object.
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(email=validated_data.get('email'),
                                        password=password,
                                        first_name=validated_data.get('first_name',''),
                                        last_name=validated_data.get('last_name',''))
        return user
    























# accounts/api/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        new_password = data.get("new_password")

        if len(new_password) < 8:
            raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long."})
        return data

    def save(self, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid UID."})

        if not token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Invalid or expired token."})

        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user