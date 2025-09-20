import logging

from rest_framework.fields import Field


from core.models import User
from rest_framework import serializers
from PIL import Image

logger = logging.getLogger(__name__)


class DBUserSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "bio",
            "avatar",
            "created_at",
        ]


class RequestUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)


class RequestUpdateUserSerializer(DBUserSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password_field: Field = self.fields.get("password")  # pyright: ignore
        password_field.read_only = True
        for fields in self.fields.values():
            fields.required = False
            fields.allow_null = True

        def validate_avatar(self, value):
            if value:
                try:
                    img = Image.open(value)
                    img.verify()  # Will raise exception if corrupted
                except (Image.UnidentifiedImageError, IOError):
                    raise serializers.ValidationError(
                        "Uploaded avatar is not a valid image."
                    )
            return value
