from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_message_to_group(group_name: str, sender: str, text: str):

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat.message",
            "message": {
                'type': 'massages',
                'content': [
                    {
                        'sender': sender,
                        'massage': text
                    }
                ]
            },
        }
    )

