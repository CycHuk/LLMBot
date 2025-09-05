from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.room_name = f"user_{user.id}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            "message": f"Привет, {user.username}!"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        user = self.scope["user"]
        message_text = text_data.strip()

        if not message_text:
            return

        last_message = await self.get_last_message(user)

        if not last_message or last_message.sender != Message.Sender.USER:
            await self.save_message(user, message_text, sender=Message.Sender.USER)
        else:
            await self.send(text_data=json.dumps({
                "type": "error",
                "content": "Дождитесь ответа"
            }))

    @database_sync_to_async
    def get_last_message(self, user):
        return Message.objects.filter(user=user).order_by('-created_at').first()

    @database_sync_to_async
    def save_message(self, user, text, sender):
        return Message.objects.create(user=user, text=text, sender=sender)

