import logging


from core.models import User
from rest_framework import serializers

logger = logging.getLogger(__name__)


class DbUserSerializer(serializers.ModelSerializer):
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


class RequestUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
