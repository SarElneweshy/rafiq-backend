import requests
from .models import Device
from .firebase import send_push_notification


ZENQUOTES_URL = "https://zenquotes.io/api/quotes/"


def get_random_quote():
    try:
        response = requests.get(ZENQUOTES_URL)
        data = response.json()

        if data:
            return data[0]['q'], data[0]['a']

        return None, None
    except Exception:
        return None, None


def send_daily_quotes():
    quote_text, author = get_random_quote()

    if not quote_text:
        return "No quote available"

    devices = Device.objects.all()

    for device in devices:
        try:
            send_push_notification(
                token=device.fcm_token,
                title="Daily Inspiration ✨",
                body=f"{quote_text} — {author}"
            )
        except Exception:
            continue

    return "Daily notifications sent"
