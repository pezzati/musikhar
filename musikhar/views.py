from django.http.response import HttpResponse
from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from loginapp.models import Device
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
            is_token_valid=False,
            url=settings.DOWNLOAD_LINKS[device_type].get('url')
        )

        if not request.user.is_anonymous:
            res['is_token_valid'] = True
            udid = data['udid']
            one_signal_id = data.get('one_signal_id')
            Device.objects.update_or_create(udid=udid,
                                            user=request.user,
                                            defaults={
                                                'one_signal_id': one_signal_id,
                                                'build_version': build_version
                                            }
                                            )

        if build_version < settings.APP_VERSION[device_type]['min']:
            res['force_update'] = True
        elif build_version < settings.APP_VERSION[device_type]['max']:
            res['suggest_update'] = True
        elif build_version > settings.APP_VERSION[device_type]['max']:
            response = Errors.get_errors(Errors, error_list=['Invalid_Build_Version'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        return Response(data=res)


def home(request):
    if request.method == 'GET':
        tmp = 'index-x1.html'
        return render(request=request, template_name=tmp)
    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
