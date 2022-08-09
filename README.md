# Django Firebase authentication

## Setup

## Required settings

* `DJANGO_FIREBASE_AUTH_AUTH_BACKEND` - Django auth backend that Firebase authentication should use.
* `DJANGO_FIREBASE_AUTH_SERVICE_ACCOUNT_FILE` - Firebase service account file for using Firebase Admin SDK.
* `DJANGO_FIREBASE_AUTH_WEB_API_KEY` - Firebase app web API key (public-facing).


## Using `django_firebase_auth` views

Register `django_firebase_auth` URLs and `django.contrib.admin.site.urls` in your project's `urls.py`, e.g.:

```
from django.contrib import admin

urlpatterns = [
    ...
    path('', include("django_firebase_auth.urls")),
    ...
    path('admin/', admin.site.urls),
    ...
]
```
Make sure to register `admin.site.urls` _after_ `django_firebase_auth` because `django_firebase_auth` uses `/admin/login` URL.