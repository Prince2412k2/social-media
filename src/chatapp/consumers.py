import json
from time import sleep
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import logging

from chatapp.models import Message
from channels.db import database_sync_to_async

logger = logging.getLogger("uvicorn.error.core")


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        logger.warning(self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "connected"}))

    async def disconnect(self, close_code):
        await self.send(text_data=json.dumps({"message": "disconnected"}))

    async def receive(self, text_data):
        if not text_data:
            return
        user_id = self.scope["url_route"]["kwargs"]["user_id"]
        try:
            await self.save_message(user_id, text_data)
        except Exception as e:
            logger.error(e)
            text_data = "Something went wrong"
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "users": user_id,
                "message": text_data,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))

    @database_sync_to_async
    def save_message(self, user_id, text):
        Message.objects.create(msg=json.dumps({"user": user_id, "msg": text}))
