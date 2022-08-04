from typing import Optional

from firebase_admin import credentials, auth, initialize_app
from firebase_admin.auth import ExpiredIdTokenError
from firebase_admin.exceptions import FirebaseError
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http.request import HttpHeaders
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import AbstractBaseUser
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse


AUTH_BACKEND = settings.DJANGO_FIREBASE_AUTH_AUTH_BACKEND
SERVICE_ACCOUNT_FILE = settings.DJANGO_FIREBASE_AUTH_SERVICE_ACCOUNT_FILE
WEB_API_KEY = settings.DJANGO_FIREBASE_AUTH_WEB_API_KEY
JWT_HEADER_NAME = getattr(settings, "DJANGO_FIREBASE_AUTH_JWT_HEADER_NAME", "X-FIREBASE-JWT")
CREATE_USER_IF_NOT_EXISTS = getattr(settings, "DJANGO_FIREBASE_AUTH_CREATE_USER_IF_NOT_EXISTS", False)
ALLOW_NOT_CONFIRMED_EMAILS = getattr(settings, "DJANGO_FIREBASE_AUTH_ALLOW_NOT_CONFIRMED_EMAILS", False)
FALLBACK_LOGIN_URL = getattr(settings, "DJANGO_FIREBASE_AUTH_FALLBACK_LOGIN_URL", None)

firebase_credentials = credentials.Certificate(SERVICE_ACCOUNT_FILE)
initialize_app(firebase_credentials)


class AuthError(Exception):
    error_type = 'OTHER'
    error_description = 'Something went wrong'

    @classmethod
    def make_response_body(cls):
        return {'error': cls.error_type, 'description': cls.error_description}


class NoAuthHeader(AuthError):
    error_type = 'NO_AUTH_HEADER'
    error_description = 'Missing Firebase authentication header'


class JWTExpired(AuthError):
    error_type = 'JWT_EXPIRED'
    error_description = 'Firebase authentication token is expired'


class JWTInvalid(AuthError):
    error_type = 'JWT_INVALID'
    error_description = 'Firebase authentication token is invalid'


class UserNotRegistered(AuthError):
    error_type = 'USER_NOT_REGISTERED'
    error_description = 'This user has not been registered'


class EmailNotVerified(AuthError):
    error_type = 'EMAIL_NOT_VERIFIED'
    error_description = 'User email has not been verified'


def authenticate(request: HttpRequest):
    try:
        email = _verify_firebase_account(request.headers)
    except AuthError as ex:
        return JsonResponse(ex.make_response_body(), status=401)

    user = _get_or_create_user(email)
    if user is None:
        return JsonResponse(UserNotRegistered.make_response_body(), status=401)

    login(request=request, user=user, backend=AUTH_BACKEND)
    return JsonResponse({"status": "ok"})


def _get_or_create_user(email: str) -> Optional[AbstractBaseUser]:
    UserModel = get_user_model()
    try:
        return UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        if not CREATE_USER_IF_NOT_EXISTS:
            return None

    user = UserModel.objects.create_user(username=email, email=email, is_active=True)
    user.set_unusable_password()
    user.save()
    return user


def _verify_firebase_account(headers: HttpHeaders) -> str:
    jwt = headers.get(JWT_HEADER_NAME)
    if jwt is None:
        raise NoAuthHeader()
    try:
        decoded_token = auth.verify_id_token(jwt)
        print(decoded_token)
    except ExpiredIdTokenError:
        raise JWTExpired()
    except FirebaseError:
        raise JWTInvalid()

    is_email_verified = decoded_token["email_verified"]
    if not is_email_verified and not ALLOW_NOT_CONFIRMED_EMAILS:
        raise EmailNotVerified()

    return decoded_token['email']


def login_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', settings.LOGIN_REDIRECT_URL))
    template = loader.get_template('firebase_authentication/login.html')
    return HttpResponse(
        template.render({
            'firebase_web_api_key': WEB_API_KEY,
            'jwt_header_name': JWT_HEADER_NAME,
            'firebase_auth_endpoint': reverse(authenticate),
            'login_redirect_url': settings.LOGIN_REDIRECT_URL,
            'django_login_url': settings.LOGIN_URL,
            'fallback_login_url': FALLBACK_LOGIN_URL,
        })
    )