from rest_framework import serializers

from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:  # pyright: ignore
        model = Comment
        fields = [
            "id",
            "user",
            "post",
            "text",
        ]


class CommentIdSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()


class CommentIdPostIdSerializer(CommentIdSerializer):
    post_id = serializers.IntegerField()
