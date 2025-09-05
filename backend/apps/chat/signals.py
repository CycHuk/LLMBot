from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from .utils import send_message_to_group


@receiver(post_save, sender=Message)
def message_created_handler(sender, instance, created, **kwargs):
    if created:
        group_name = f'chat_{instance.user_id}'
        sender = instance.sender
        text = instance.text

        send_message_to_group(group_name, sender, text)

