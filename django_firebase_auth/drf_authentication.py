from django.utils.functional import SimpleLazyObject
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django_firebase_auth.conf import user_getter
from django_firebase_auth.views import verify_firebase_account, AuthError, NoAuthHeader


class LazyUser(SimpleLazyObject):
    is_authenticated = True
    is_anonymous = False

    def __bool__(self):
        return True


class JWTAuthentication(BaseAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """
        try:
            jwt_payload = verify_firebase_account(request.headers)
        except NoAuthHeader:
            return None
        except AuthError as ex:
            raise AuthenticationFailed(code=ex.error_type, detail=ex.error_type)
        return LazyUser(lambda: user_getter.get_or_create_user(jwt_payload)), None
