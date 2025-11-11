from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .cron import run_check
from .models import TemperatureReading
from .serializers import TemperatureReadingSerializer

class TriggerFetchView(APIView):
    def get(self, request):
        token = request.headers.get("X-API-KEY") or request.query_params.get("token")
        if token != settings.API_TEST_TOKEN:
            return Response({"detail": "invalid token"}, status=status.HTTP_403_FORBIDDEN)

        # Force a execução mesmo dentro de janela CHECK_EVERY_MIN
        run_check(force=True)

        return Response({"status": "ok"})

class LatestView(APIView):
    """Retorna a última leitura registrada."""

    def get(self, request):
        obj = TemperatureReading.objects.order_by("-when").first()
        if not obj:
            return Response({"latest": None})
        return Response(TemperatureReadingSerializer(obj).data)
