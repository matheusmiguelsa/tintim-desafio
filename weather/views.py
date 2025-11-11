from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .cron import run_check
from .models import TemperatureReading
from .serializers import TemperatureReadingSerializer


class TriggerFetchView(APIView):
    """Força a coleta de dados e valida o token de acesso."""

    def get(self, request):
        token = request.headers.get("X-API-KEY") or request.query_params.get("token")
        if token != settings.API_TEST_TOKEN:
            return Response({"detail": "invalid token"}, status=status.HTTP_403_FORBIDDEN)

        run_check(force=True)
        return Response({"status": "ok"})


class LatestView(APIView):
    """Retorna a última leitura registrada."""

    def get(self, _):
        obj = TemperatureReading.objects.order_by("-when").first()
        return (
            Response(TemperatureReadingSerializer(obj).data)
            if obj else Response({"latest": None})
        )
