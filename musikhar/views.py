from django.dispatch import receiver
from django.http.response import HttpResponse
from django.shortcuts import render
#from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from constance import config
from constance.signals import config_updated


from loginapp.models import Device
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import Errors, send_onesignal_notification


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
            url={'url': config.iOS_SIBAPP_DL} if device_type == 'ios' else config.ANDROID_DL
        )

        if not request.user.is_anonymous:
            res['is_token_valid'] = True
            udid = data.get('udid', 'not-set')
            one_signal_id = data.get('one_signal_id')
            Device.objects.update_or_create(udid=udid,
                                            user=request.user,
                                            defaults={
                                                'one_signal_id': one_signal_id,
                                                'build_version': build_version,
                                                'type': device_type

                                            }
                                            )
        else:
            res['is_token_valid'] = False
            udid = data.get('udid', 'not-set')
            one_signal_id = data.get('one_signal_id')
            Device.objects.update_or_create(udid=udid,
                                            defaults={
                                                'one_signal_id': one_signal_id,
                                                'build_version': build_version,
                                                'type': device_type
                                            }
                                            )
        if device_type == 'ios':
            max_version = config.iOS_MAX
            min_version = config.iOS_MIN
        else:
            max_version = config.ANDROID_MAX
            min_version = config.ANDROID_MIN

        if build_version < min_version:
            res['force_update'] = True
        elif build_version < max_version:
            res['suggest_update'] = True
        elif build_version > max_version:
            response = Errors.get_errors(Errors, error_list=['Invalid_Build_Version'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

        return Response(data=res)


def home(request):
    if request.method == 'GET':
        tmp = 'index-x1.html'
        return render(request, tmp, {'config': config})
    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @receiver(config_updated)
# def constance_updated(sender, key, old_value, new_value, **kwargs):
#     if key == 'iOS_MAX':
#
#         send_onesignal_notification()
#         pass
#     print(sender, key, old_value, new_value)
