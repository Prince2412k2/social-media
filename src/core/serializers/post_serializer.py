import logging
from rest_framework import serializers

from core.models import Post
from core.serializers.comment_serializer import CommentSerializer

logger = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:  # pyright: ignore
        model = Post
        fields = [
            "id",
            "user",
            "user_id",
            "is_followed",
            "image",
            "caption",
            "likes_count",
            "liked_by_user",
            "comments",
        ]

    def get_likes_count(self, obj):
        # use cached field or count M2M
        return obj.likes_count or obj.liked_by.count()

    def get_liked_by_user(self, obj):
        request = self.context.get("request", None)
        if request:
            user = request.user  # pyright: ignore
            return obj.liked_by.filter(id=user.id)
        return False

    def get_user_id(self, obj):
        return obj.user.pk

    def get_is_followed(self, obj):
        self_user = self.context.get("self_user")
        if self_user:
            return self_user.is_following(obj.user)
        return None


class GetPostSerializer(serializers.Serializer):
    user = serializers.StringRelatedField(read_only=True)
    posts = serializers.SerializerMethodField()

    class Meta:  # pyright: ignore
        model = Post
        fields = [
            "id",
            "posts",
        ]

    def get_posts(self, obj):
        request = self.context.get("request")
        if request:
            return request.user.posts.count()
        return 0


class PostIdSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
