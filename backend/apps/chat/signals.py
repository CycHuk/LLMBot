from celery.signals import task_success
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from .utils import send_message_to_group
from .tasks import send_message_task
from ..account.models import User


@receiver(post_save, sender=Message)
def message_created_handler(sender, instance, created, **kwargs):
    if created:
        group_name = f'chat_{instance.user_id}'
        sender = instance.sender
        text = instance.text

        send_message_to_group(group_name, sender, text)

        if sender == 'user':
            send_message_task.delay(instance.user_id, text)


@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):

    if sender.name == 'apps.chat.tasks.send_message_task':
        user_id = result['user_id']
        sender = result['sender']
        text = result['text']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return

        Message.objects.create(
            user=user,
            text=text,
            sender=sender
        )



