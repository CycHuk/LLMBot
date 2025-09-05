from django.db import models
import uuid

from django.db import models
import uuid


class Message(models.Model):
    class Sender(models.TextChoices):
        USER = 'user', 'User'
        BOT = 'bot', 'Bot'
        SYSTEM = 'system', 'System'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('account.User', related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    sender = models.CharField(max_length=10, choices=Sender.choices, default=Sender.USER)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}"
