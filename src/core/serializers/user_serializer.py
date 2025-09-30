import logging

from rest_framework.fields import Field


from core.models import User
from rest_framework import serializers
from PIL import Image

from core.services.post_service import PostService
from core.services.user_services import FollowService, UserService

logger = logging.getLogger(__name__)


class DBUserSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    class Meta:  # pyright: ignore
        model = User
        fields = [
            "id",
            "username",
            "follower_count",
            "following_count",
            "post_count",
            "password",
            "email",
            "bio",
            "avatar",
            "created_at",
        ]

    def get_follower_count(self, obj):
        return FollowService.get_followers_count(obj)

    def get_following_count(self, obj):
        return FollowService.get_following_count(obj)

    def get_post_count(self, obj):
        return UserService.get_post_count(obj)


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
