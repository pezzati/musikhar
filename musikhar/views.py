# from django.dispatch import receiver
import ast
from django.http.response import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from constance import config
# from constance.signals import config_updated
from ddtrace import patch

from loginapp.models import Device, User, Token
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import Errors, app_logger, conn, convert_to_dict, get_not_none
import random
patch()


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
            url=config.iOS_SIBAPP_DL if device_type == 'ios' else config.ANDROID_DL,
            token=''
        )

        udid = data.get('udid', 'not-set')
        one_signal_id = data.get('one_signal_id')
        bundle = get_not_none(data, 'bundle', 'com.application.canto')
        if not request.user.is_anonymous:
            res['is_token_valid'] = True
            Device.objects.update_or_create(udid=udid,
                                            bundle=bundle,
                                            user=request.user,
                                            defaults={
                                                'one_signal_id': one_signal_id,
                                                'build_version': build_version,
                                                'type': device_type

                                            }
                                            )
        else:
            if build_version == config.iOS_MAX and random.random() < 0.4:
                user = User.create_guest_user()
                token = Token.generate_guest_token(user=user)
                res['token'] = token.key
                res['is_token_valid'] = True
                Device.objects.create(udid=udid,
                                      user=user,
                                      bundle=bundle,
                                      one_signal_id=one_signal_id,
                                      build_version=build_version,
                                      type=device_type
                                      )
            else:
                res['is_token_valid'] = False
                # udid = data.get('udid', 'not-set')
                # one_signal_id = data.get('one_signal_id')
                Device.objects.create(udid=udid,
                                      bundle=bundle,
                                      one_signal_id=one_signal_id,
                                      build_version=build_version,
                                      type=device_type
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

        if res['force_update'] or res['suggest_update']:
            res['update_log'] = config.iOS_UPDATE_LOG if device_type == 'ios' else config.ANDROID_UPDATE_LOG

        return Response(data=res)


def home(request):
    app_logger.info('[APP_TEST]')
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

class Repeater(IgnoreCsrfAPIView):
    def post(self, request):
        if settings.DEBUG:
            return Response(status=status.HTTP_410_GONE)
        if not request.user or not request.user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'msg': 'You must be superuser'})
        data = request.data
        conn().set(name='repeater', value=convert_to_dict(data))
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        if settings.DEBUG:
            return Response(status=status.HTTP_410_GONE)
        raw_data = conn().get('repeater')
        if raw_data:
            try:
                return Response(ast.literal_eval(raw_data.decode('utf-8')))
            except:
                return Response()


@csrf_exempt
def bazzar(request):
    res = '{}'.format(request.body)
    return HttpResponse(res)
