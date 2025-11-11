from django.db import models
from django.utils import timezone

class Settings(models.Model):
    temp_limit_c = models.FloatField(default=30.0)
    check_every_min = models.PositiveIntegerField(default=30)
    lat = models.FloatField(default=-23.55)
    lon = models.FloatField(default=-46.63)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Config(limite={self.temp_limit_c}C, {self.check_every_min}min)"

class TemperatureReading(models.Model):
    when = models.DateTimeField(default=timezone.now)
    temp_c = models.FloatField()
    source = models.CharField(max_length=50, default='open-meteo')

    def __str__(self):
        return f"{self.when:%Y-%m-%d %H:%M} -> {self.temp_c}C"

class Alert(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    temp_c = models.FloatField()
    limit_c = models.FloatField()
    message = models.TextField()

    def __str__(self):
        return f"ALERTA {self.created_at:%Y-%m-%d %H:%M}: {self.temp_c}C > {self.limit_c}C"
