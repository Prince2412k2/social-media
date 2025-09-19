from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate(self, attrs: dict):
        self_user_id = self.context["request"].user.id
        other_user = attrs["user_id"]
        if self_user_id == other_user:
            raise ValidationError("Following/Unfollowing yourself is not allowed")
        return attrs
