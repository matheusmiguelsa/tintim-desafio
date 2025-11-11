from django.conf import settings
from django.core.mail import send_mail
import requests


def notify_email(subject: str, body: str):
    recipient = settings.NOTIFY_EMAIL_TO or settings.EMAIL_HOST_USER
    if not recipient:
        return
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=True)


def notify_telegram(text: str):
    if not (settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID):
        return

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": text}, timeout=10)
