from django.urls import re_path

from .views import authenticate, LoginView

urlpatterns = [
    re_path(r'api/v1/login/?$', authenticate),
    re_path(r'login/?$', LoginView.as_view()),
]
