from django.urls import re_path

from ..views import authenticate, AdminLoginView, logout

urlpatterns = [
    re_path(r'firebase_authentication/v1/login/?$', authenticate),
    re_path(r'firebase_authentication/v1/logout/?$', logout),
    re_path(r'admin/login/?$', AdminLoginView.as_view()),
]
