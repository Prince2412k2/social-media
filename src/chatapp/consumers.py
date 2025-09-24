import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import logging

logger = logging.getLogger("uvicorn.error.core")


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "connected"}))

    async def disconnect(self, close_code):
        await self.send(text_data=json.dumps({"message": "disconnected"}))

    async def receive(self, text_data: str):
        logger.info(type(text_data))
        if not text_data:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": text_data,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
