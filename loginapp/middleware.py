import json
from django.contrib import auth
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

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


class ExpiredVersionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            build_version = int(request.META.get('HTTP_BUILDVERSION'))
            device_type = request.META.get('HTTP_DEVICETYPE')
            if build_version < settings.APP_VERSION[device_type]['min']:
                return HttpResponse(json.dumps(settings.DOWNLOAD_LINKS[device_type]),
                                    status=426,
                                    content_type="application/json")
        except TypeError:
            if request.path.startswith('/admin/'):
                pass
