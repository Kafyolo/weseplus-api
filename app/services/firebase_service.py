import os
import firebase_admin
from firebase_admin import credentials, messaging
from app.core.config import settings

class FirebaseService:
    def __init__(self):
        if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            self.enabled = True
        else:
            print(f"WARNING: Firebase credentials not found at {settings.FIREBASE_CREDENTIALS_PATH}. Firebase features disabled.")
            self.enabled = False

    def send_sms_otp(self, phone: str, otp: str):
        # In a real scenario, this would trigger an SMS via FCM or a third-party gateway
        # linked to Firebase. For this implementation, we log the intent.
        message = f"Simulating SMS to {phone}: Karibu WesePlus. Msimbo wako wa siri ni {otp}. Usimpe mtu yeyote."
        print(message)
        # return self.log_analytics_event("otp_sent", {"phone": phone})

    def log_analytics_event(self, event_name: str, parameters: dict):
        # Firebase Analytics is typically for client-side (app) tracking.
        # Server-side 'analytics' often goes to BigQuery but we can simulate it.
        print(f"FIREBASE_ANALYTICS: Event: {event_name}, Params: {parameters}")
        # if self.enabled:
        #     # Logic for server-side logging if required
        #     pass

    def send_notification(self, phone: str, title: str, body: str):
        print(f"NOTIFY: {phone} - {title}: {body}")
        # if self.enabled:
        #     # Logic to send FCM if token exists
        #     pass

firebase_service = FirebaseService()
