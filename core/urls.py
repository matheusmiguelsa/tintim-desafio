from django.contrib import admin
from django.urls import path
from weather.views import TriggerFetchView, LatestView
from weather.views_webhooks import telegram_webhook
from weather.views_webhooks import n8n_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trigger-fetch/', TriggerFetchView.as_view(), name='trigger-fetch'),
    path('api/latest/', LatestView.as_view(), name='latest'),
    path("api/webhook/telegram/", telegram_webhook),
    path("api/webhook/n8n/", n8n_webhook),

]
