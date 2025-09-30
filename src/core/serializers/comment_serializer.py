from rest_framework import serializers

from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()

    class Meta:  # pyright: ignore
        model = Comment
        fields = ["id", "user_id", "post", "text", "user_profile"]

    def get_user_profile(self, obj):
        avatar = obj.user.avatar
        return avatar.url if avatar else None


class CommentIdSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
