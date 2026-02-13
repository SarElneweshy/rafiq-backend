import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import os

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate(
        os.path.join(settings.BASE_DIR, "firebase_key.json")
    )
    firebase_admin.initialize_app(cred)


def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    response = messaging.send(message)
    return response
