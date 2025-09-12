from rest_framework import serializers

from core.auth.password_service import set_password
from .models import User


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
        password = validated_data.pop("password", None)
        user = User.objects.create(**validated_data)

        if provider == "PASSWORD":
            set_password(user, password)
        elif provider == "GOOGLE":
            pass
        elif provider == "GITHUB":
            pass
        return user


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = User
        fields = ["id", "user", "provider", "provider_id", "password", "created_at"]
