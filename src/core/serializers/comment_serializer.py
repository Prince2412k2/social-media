from rest_framework import serializers

from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
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
