from django.test import TestCase
from rest_framework.test import APIClient
from django.conf import settings
from unittest.mock import patch
from .models import Settings, TemperatureReading, Alert

class WeatherFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("weather.services.get_current_temp", return_value=35.0)
    def test_alert_when_over_limit(self, mock_temp):
        Settings.objects.create(temp_limit_c=30, check_every_min=1, lat=0, lon=0)
        # token válido
        resp = self.client.get("/api/trigger-fetch/", HTTP_X_API_KEY=settings.API_TEST_TOKEN)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(TemperatureReading.objects.exists())
        self.assertTrue(Alert.objects.exists())

    @patch("weather.services.get_current_temp", return_value=20.0)
    def test_no_alert_when_below_limit(self, mock_temp):
        Settings.objects.create(temp_limit_c=30, check_every_min=1, lat=0, lon=0)
        resp = self.client.get("/api/trigger-fetch/", HTTP_X_API_KEY=settings.API_TEST_TOKEN)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(TemperatureReading.objects.exists())
        self.assertFalse(Alert.objects.exists())

    def test_trigger_requires_token(self):
        resp = self.client.get("/api/trigger-fetch/")
        self.assertEqual(resp.status_code, 403)

    @patch("weather.services.get_current_temp", return_value=22.0)
    def test_latest_endpoint(self, mock_temp):
        Settings.objects.create(temp_limit_c=30, check_every_min=1, lat=0, lon=0)
        self.client.get("/api/trigger-fetch/", HTTP_X_API_KEY=settings.API_TEST_TOKEN)
        resp = self.client.get("/api/latest/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("temp_c", resp.json())
