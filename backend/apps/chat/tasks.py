from celery import shared_task
import random
import time


@shared_task
def send_message_task(user_id, text):
    time.sleep(3)
    sender = random.choice(['system', 'bot'])
    return {'user_id': user_id, 'sender':sender, 'text': text}