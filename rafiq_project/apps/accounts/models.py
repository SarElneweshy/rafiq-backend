from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _generate_unique_username(self, base: str):
        UserModel = self.model
        username = base

        if not username:
            username = "user"

        while UserModel.objects.filter(username=username).exists():
            username = f"{base or 'user'}_{get_random_string(6)}"
        return username

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        provided_username = extra_fields.pop("username", None)
        if provided_username:
            username = provided_username
            
            if self.model.objects.filter(username=username).exists():
                username = f"{username}_{get_random_string(6)}"
        else:
            base = email.split("@")[0] if "@" in email else email
            username = self._generate_unique_username(base)

        extra_fields["username"] = username

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
