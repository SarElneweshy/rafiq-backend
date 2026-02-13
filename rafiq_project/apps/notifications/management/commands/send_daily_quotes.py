from django.core.management.base import BaseCommand
from apps.notifications.utils import send_daily_quotes


class Command(BaseCommand):
    help = "Send daily inspirational quotes"

    def handle(self, *args, **kwargs):
        result = send_daily_quotes()
        self.stdout.write(self.style.SUCCESS(result))
