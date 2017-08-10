from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin

from loginapp.models import Token


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get('HTTP_USERTOKEN') or \
                request.COOKIES.get('user_token') or \
                request.GET.get('t')
        token = Token.objects.filter(key=token).first()
        user = auth.authenticate(token=token)

        if user:
            request.user = user
            request._token = token.key

        else:
            request._token = ''