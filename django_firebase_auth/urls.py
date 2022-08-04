from django.urls import re_path

from .views import authenticate, login_page

urlpatterns = [
    re_path(r'api/v1/login/?$', authenticate),
    re_path(r'login/?$', login_page),
]
