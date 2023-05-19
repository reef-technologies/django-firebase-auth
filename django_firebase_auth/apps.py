from django.apps import AppConfig
from firebase_admin import credentials, initialize_app

from django_firebase_auth.conf import SERVICE_ACCOUNT_FILE


class DjangoFirebaseAuthConfig(AppConfig):
    name = 'django_firebase_auth'

    def ready(self):
        if SERVICE_ACCOUNT_FILE:
            firebase_credentials = credentials.Certificate(SERVICE_ACCOUNT_FILE)
            initialize_app(firebase_credentials)