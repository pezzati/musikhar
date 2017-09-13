from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import Errors


class Handshake(IgnoreCsrfAPIView):

    def post(self, request):
        data = request.data
        device_type = data.get('device_type')
        if not device_type:
            response = Errors.get_errors(Errors, error_list=['Missing_Type'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)
        if device_type != 'android' and device_type != 'ios':
            response = Errors.get_errors(Errors, error_list=['Invalid_Type'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        build_version = data.get('build_version')
        try:
            build_version = int(build_version)
        except TypeError:
            build_version = 0

        res = dict(
            force_update=False,
            suggest_update=False,
            is_token_valid=False
        )

        if not request.user.is_anonymous:
            res['is_token_valid'] = True

        if build_version < settings.APP_VERSION[device_type]['min']:
            res['force_update'] = True
        elif build_version < settings.APP_VERSION[device_type]['max']:
            res['suggest_update'] = True
        elif build_version > settings.APP_VERSION[device_type]['max']:
            response = Errors.get_errors(Errors, error_list=['Invalid_Build_Version'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        return Response(data=res)
