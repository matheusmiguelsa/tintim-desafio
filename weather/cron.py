from datetime import timedelta
from django.utils import timezone
from django.conf import settings as dj
from .models import Settings, TemperatureReading, Alert
from .notify import notify_email, notify_telegram
import weather.services as weather_services


_last_run = None


def run_check(force=False):
    global _last_run
    now = timezone.now()

    # garante o Settings
    cfg, _ = Settings.objects.get_or_create(
        id=1,
        defaults={
            "temp_limit_c": dj.TEMP_LIMIT_C,
            "check_every_min": dj.CHECK_EVERY_MIN,
            "lat": dj.WEATHER_LAT,
            "lon": dj.WEATHER_LON,
        }
    )

    # IGNORA CHECK_EVERY_MIN durante testes
    if not force:
        if _last_run and now - _last_run < timedelta(minutes=cfg.check_every_min):
            return

    _last_run = now

    temp = weather_services.get_current_temp(cfg.lat, cfg.lon)
    reading = TemperatureReading.objects.create(temp_c=temp)

    if temp > cfg.temp_limit_c:
        msg = f"Temperatura {temp:.1f}°C ultrapassou o limite {cfg.temp_limit_c:.1f}°C."
        Alert.objects.create(temp_c=temp, limit_c=cfg.temp_limit_c, message=msg)
        notify_email("Alerta de Temperatura", msg)
        notify_telegram(msg)

    return reading
