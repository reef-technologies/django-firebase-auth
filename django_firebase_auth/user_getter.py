import abc
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser


class UserNotFound(Exception):
    pass


class AbstractUserGetter(abc.ABC):
    """
    Base class for implementing user getters: pluggable classes facilitating user fetching and creation based on
    firebase JWT payload.
    """

    def __init__(self, create_if_not_exists: bool):
        self.create_if_not_exists = create_if_not_exists

    @abc.abstractmethod
    def _get_user(self, jwt_payload) -> Optional[AbstractBaseUser]: ...

    @abc.abstractmethod
    def _create_user(self, jwt_payload) -> AbstractBaseUser: ...

    def get_or_create_user(self, jwt_payload: dict) -> AbstractBaseUser:
        """
        get or, depending on self.create_if_not_exists, create a user. This method always returns a user or raises
        UserNotFound.
        :param jwt_payload: dict obtained by decoding firebase JWT
        :return: a user
        """
        user = self._get_user(jwt_payload)
        if user is None and not self.create_if_not_exists:
            raise UserNotFound
        if user is not None:
            return user
        return self._create_user(jwt_payload)


class SimpleUserGetter(AbstractUserGetter):
    use_email_as_username = True

    def __init__(self, create_if_not_exists: bool):
        super().__init__(create_if_not_exists)
        self.UserModel = get_user_model()

    def _get_user(self, jwt_payload) -> Optional[AbstractBaseUser]:
        try:
            return self.UserModel.objects.get(email=jwt_payload['email'])
        except self.UserModel.DoesNotExist:
            return None

    def _create_user(self, jwt_payload) -> AbstractBaseUser:
        user = self.UserModel.objects.create_user(
            email=jwt_payload['email'],
            is_active=True,
            **({"username": jwt_payload['email']} if self.use_email_as_username else {})
        )
        user.set_unusable_password()
        user.save()
        return user


class EmailOnlyUserGetter(SimpleUserGetter):
    use_email_as_username = False
