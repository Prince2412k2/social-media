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
