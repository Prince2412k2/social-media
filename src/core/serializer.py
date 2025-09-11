from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = User
        fields = ["id", "username", "email", "bio", "avatar", "created_at"]


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = User
        fields = ["id", "user", "provider", "provider_id", "password", "created_at"]
