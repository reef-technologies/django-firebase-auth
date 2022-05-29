import json

import firebase_admin
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.http.request import HttpHeaders
from django.conf import settings
from django.contrib.auth import login
from firebase_admin import credentials, auth
from firebase_admin.auth import ExpiredIdTokenError
from firebase_admin.exceptions import FirebaseError

if settings.GOOGLE_SERVICE_ACCOUNT_FILE:
    firebase_credentials = credentials.Certificate(settings.GOOGLE_SERVICE_ACCOUNT_FILE)
    firebase_admin.initialize_app(firebase_credentials)

HEADER = 'X-FIREBASE-JWT'


class AuthError(Exception):
    error_type = 'OTHER'

    @classmethod
    def make_response_body(cls):
        return {'error_type': cls.error_type}


class NoAuthHeader(AuthError):
    error_type = 'NO_AUTH_HEADER'


class JWTExpired(AuthError):
    error_type = 'JWT_EXPIRED'


class JWTInvalid(AuthError):
    error_type = 'JWT_INVALID'


class UserNotRegistered(AuthError):
    error_type = 'USER_NOT_REGISTERED'


class EmailNotVerified(AuthError):
    error_type = 'EMAIL_NOT_VERIFIED'


def _get_firebase_email(headers: HttpHeaders):
    jwt = headers.get(HEADER)
    if jwt is None:
        raise NoAuthHeader()
    try:
        decoded_token = auth.verify_id_token(jwt)
    except ExpiredIdTokenError:
        raise JWTExpired()
    except FirebaseError:
        raise JWTInvalid()
    return decoded_token['email']


def authenticate(request: HttpRequest):
    try:
        email = _get_firebase_email(request.headers)
    except AuthError as ex:
        return HttpResponse(json.dumps(ex.make_response_body()).encode(), status=401)

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return HttpResponse(json.dumps(UserNotRegistered.make_response_body()).encode(), status=401)

    login(request=request, user=user, backend=settings.FIREBASE_AUTH_BACKEND)
    return HttpResponse(b'ok', status=200)
