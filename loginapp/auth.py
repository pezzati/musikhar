from django.core.exceptions import PermissionDenied
from .models import User, Token


class AuthBackend(object):
    def authenticate(self, token=None):
        if not token:
            return None

        try:
            if not isinstance(token, Token):
                token = Token.objects.get(key=token)

            if token.is_valid():
                return token.user

            return None

        except Token.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def if_authorized(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return function(request, *args, **kwargs)

        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap