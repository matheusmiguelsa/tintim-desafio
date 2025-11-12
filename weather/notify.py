from django.conf import settings
from django.core.mail import send_mail
import requests


def notify_n8n(message):
    """Dispara webhook para o n8n"""
    url = getattr(settings, "N8N_WEBHOOK_URL", "")

    if not url:
        return  # Sem URL definida, não envia

    try:
        requests.post(url, json={"alert": message}, timeout=10)
    except Exception as e:
        print(f"[n8n] erro ao enviar: {e}")

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
