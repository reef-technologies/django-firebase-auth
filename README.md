# Django Firebase authentication

## Setup

## Required settings

* `DJANGO_FIREBASE_AUTH_AUTH_BACKEND` - Django auth backend that Firebase authentication should use. Required.
* `DJANGO_FIREBASE_AUTH_SERVICE_ACCOUNT_FILE` - Firebase service account file for using Firebase Admin SDK. Required.
* `DJANGO_FIREBASE_AUTH_WEB_API_KEY` - Firebase app web API key (public-facing). Required.


## Using `django_firebase_auth` views

Register `django_firebase_auth` URLs in your project's `urls.py`, e.g.:

```
urlpatterns = [
    ...
    path('firebase_authentication/', include("django_firebase_auth.urls")),
    ...
]
```

If you want Firebase authentication page to be your default login page, configure this in your `settings.py`:

```
LOGIN_URL = '/firebase_authentication/login`
```

If you want Firebase SSO login page to have a fallback link to a different login page, set:

```
DJANGO_FIREBASE_AUTH_FALLBACK_LOGIN_URL = '/your-fallback-login-page'
```
