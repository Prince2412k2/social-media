import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

from django.contrib.auth import get_user_model

from chatapp.models import Conversation, Message
from channels.db import database_sync_to_async

from chatapp.utils import get_room_name, get_token_from_scope, get_user_from_jwt

logger = logging.getLogger("uvicorn.error.core")


User = get_user_model()


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        other_user_id = (
            self.scope.get("url_route", {}).get("kwargs", {}).get("other_user_id", None)
        )
        try:
            self.token = await get_token_from_scope(self.scope)
            self.user = await get_user_from_jwt(self.token)
            self.other_user = await self.get_user_object(other_user_id)
            if not self.other_user:
                raise ValueError
        except Exception:
            await self.close()
            return

        if not self.other_user:
            await self.close()
            return

        # Generate the consistent room name
        self.room_group_name = await get_room_name(self.user.pk, self.other_user.pk)

        # Get or create the conversation object
        self.conversation = await self.get_or_create_conversation()

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):  # pyright: ignore
        data = json.loads(text_data)
        message_content = data["message"]

        # Save the message to the database ??
        await self.save_message(message_content)

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_content,
                "sender_id": self.user.pk,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {"message": event["message"], "sender_id": event["sender_id"]}
            )
        )

    async def disconnect(self, close_code):  # pyright: ignore
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # === Database Helper Methods ===

    @database_sync_to_async
    def get_user_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_or_create_conversation(self):
        assert self.other_user
        # Look for a conversation with exactly these two participants
        conversation = (
            Conversation.objects.filter(participants=self.user)
            .filter(participants=self.other_user)
            .first()
        )
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(self.user, self.other_user)
        return conversation

    @database_sync_to_async
    def save_message(self, content):
        # Create a new message object and save it
        Message.objects.create(
            conversation=self.conversation, sender=self.user, content=content
        )
