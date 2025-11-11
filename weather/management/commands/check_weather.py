from django.core.management.base import BaseCommand
from weather.cron import run_check

class Command(BaseCommand):
    help = "Executa uma verificação de temperatura (uma vez)."

    def handle(self, *args, **kwargs):
        run_check()
        self.stdout.write(self.style.SUCCESS("Weather check done."))
