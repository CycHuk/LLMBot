# backend/apps/chat/utils.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def send_message_to_group(group_name: str, msg_type: str, content: str):

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat.message",
            "msg_type": msg_type,
            "content": content
        }
    )
