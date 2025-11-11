import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weather.cron import run_check
from weather.models import TemperatureReading

TELEGRAM_SEND_MESSAGE = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"


def telegram_reply(chat_id, text):
    requests.post(TELEGRAM_SEND_MESSAGE, json={
        "chat_id": chat_id,
        "text": text
    })



@api_view(["POST"])
def n8n_webhook(request):
    """
    Recebe dados do n8n (JSON) e envia alerta para Telegram ou email
    """
    payload = request.data

    text = payload.get("text") or "Webhook recebido do n8n ✅"
    chat_id = settings.TELEGRAM_CHAT_ID

    if chat_id:
        telegram_reply(chat_id, f"📩 Webhook do n8n:\n{text}")

    return Response({"status": "received", "payload": payload})


@api_view(["POST"])
def telegram_webhook(request):
    message = request.data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").lower()

    if not chat_id:
        return Response({"error": "no chat id"}, status=400)

    if text == "/status":
        last = TemperatureReading.objects.order_by("-when").first()
        if last:
            telegram_reply(chat_id, f"🌡️ Temperatura: {last.temp_c}°C")
        else:
            telegram_reply(chat_id, "Ainda não há registros.")
        return Response({"ok": True})

    if text == "/forcar_leitura":
        run_check()
        telegram_reply(chat_id, "✅ Leitura forçada com sucesso")
        return Response({"ok": True})

    telegram_reply(chat_id, "🤖 Comandos disponíveis:\n/status\n/forcar_leitura")
    return Response({"ok": True})
