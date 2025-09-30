from rest_framework import serializers

from chatapp.models import Message
from core.models import User
from core.serializers import user_serializer


class InboxSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = Message
        fields = "__all__"
