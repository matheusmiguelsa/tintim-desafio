from django.contrib import admin
from .models import Settings, TemperatureReading, Alert

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("temp_limit_c", "check_every_min", "lat", "lon", "updated_at")

@admin.register(TemperatureReading)
class TemperatureReadingAdmin(admin.ModelAdmin):
    list_display = ("when", "temp_c", "source")
    list_filter = ("source",)
    ordering = ("-when",)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("created_at", "temp_c", "limit_c")
    ordering = ("-created_at",)
