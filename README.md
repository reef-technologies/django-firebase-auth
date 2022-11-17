# Django Firebase authentication

## Setup

## Required settings

* `DJANGO_FIREBASE_AUTH_SERVICE_ACCOUNT_FILE` - Firebase service account file for using Firebase Admin SDK. - it can 
  be `None` which will make the app to load without a service account file but all authentication attempts will cause
  an unhandled error
* `DJANGO_FIREBASE_AUTH_AUTH_BACKEND` - Django auth backend that Firebase authentication should use.
* `DJANGO_FIREBASE_AUTH_WEB_API_KEY` - Firebase configuration app web API key (public-facing).
* `DJANGO_FIREBASE_AUTH_AUTH_DOMAIN` - Firebase configuration app auth domain.

## Optional settings

* `DJANGO_FIREBASE_AUTH_JWT_HEADER_NAME`, default=`X-FIREBASE-JWT`
* `DJANGO_FIREBASE_AUTH_CREATE_USER_IF_NOT_EXISTS`, default=`False`
* `DJANGO_FIREBASE_AUTH_ALLOW_NOT_CONFIRMED_EMAILS`, default=`False`
* `DJANGO_FIREBASE_AUTH_ENABLE_GOOGLE_LOGIN`, default=`True`
* `DJANGO_FIREBASE_AUTH_GET_OR_CREATE_USER_CLASS`, default=`django_firebase_auth.user_getter:EmailOnlyUserGetter`


## Using `django_firebase_auth` views

Register `django_firebase_auth` URLs and `django.contrib.admin.site.urls` in your project's `urls.py`, e.g.:

```
from django.contrib import admin

urlpatterns = [
    ...
    path('', include("django_firebase_auth.v0.urls")),
    ...
    path('admin/', admin.site.urls),
    ...
]
```
Make sure to register `admin.site.urls` _after_ `django_firebase_auth` because `django_firebase_auth` uses `/admin/login` URL.