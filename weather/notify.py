from django.conf import settings
from django.core.mail import send_mail
import requests

def notify_email(subject: str, body: str):
    to = settings.NOTIFY_EMAIL_TO or settings.EMAIL_HOST_USER
    if not to:
        return
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to], fail_silently=True)
    except Exception:
        pass

def notify_telegram(text: str):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not (token and chat_id):
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=15)
    except Exception:
        pass
