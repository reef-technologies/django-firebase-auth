from django.urls import re_path

from .views import authenticate, AdminLoginView

urlpatterns = [
    re_path(r'firebase_authentication/v1/login/?$', authenticate),
    re_path(r'admin/login/?$', AdminLoginView.as_view()),
]
