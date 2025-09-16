import logging
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import make_password
from ..models import User, Credential
from .password_service import check_password, verify_password
from django.contrib.auth import authenticate

# serializers.py
from dj_rest_auth.serializers import LoginSerializer
from allauth.account import app_settings
from rest_framework import serializers

logger = logging.getLogger(__name__)


class CredentialBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):  # pyright: ignore
        user = User.objects.get(email=email)
        is_valid = verify_password(user, password)
        if is_valid:
            logger.info(f"Validation Sucess : {user.id=} logged in")  # pyright: ignore
        else:
            logger.info("Validation Failed: wrong password")
        return user if is_valid else None

    def get_user(self, user_id: int):  # pyright: ignore
        try:
            logger.info("inside get_user method")
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None


class CustomRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        try:
            user = User.objects.create(
                email=validated_data["email"],
                username=validated_data["username"],
                password=make_password(validated_data["password"]),
            )
            return user
        except Exception as e:
            logger.info(f"User with {self.email=} already exists")
            raise e


class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True)
    username = None

    def authenticate(self, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")
        return authenticate(email=email, password=password)
