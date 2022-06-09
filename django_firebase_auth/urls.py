from django.urls import re_path

from .views import authenticate

urlpatterns = [
    re_path(r'firebase_authentication/v1/login/?$', authenticate),
]
