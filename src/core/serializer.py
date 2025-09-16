import logging
from rest_framework import serializers

from .models import User

from dj_rest_auth.serializers import JWTSerializer
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    provider = serializers.ChoiceField(
        choices=[
            "PASSWORD",
            # "GOOGLE",
            # "GITHUB",
        ],
        write_only=True,
        required=True,
    )

    class Meta:  # pyright: ignore
        model = User
        fields = [
            "id",
            "username",
            "password",
            "provider",
            "email",
            "bio",
            "avatar",
            "created_at",
        ]

    def create(self, validated_data):
        provider = validated_data.pop("provider")
        user = User.objects.create(**validated_data)
        if provider == "GOOGLE":
            pass
        elif provider == "GITHUB":
            pass
        return user


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = User
        fields = ["id", "user", "provider", "provider_id", "password", "created_at"]


class CustomJWTSerializer(JWTSerializer):
    def validate(self, attrs):
        return {}
