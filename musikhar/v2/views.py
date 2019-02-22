# from django.dispatch import receiver
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from constance import config

from loginapp.models import Device, User, Token
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import Errors, get_not_none
import random
# patch()


class HandshakeV2(IgnoreCsrfAPIView):
    @staticmethod
    def _is_last_version(device_type, version):
        if device_type == 'ios' and version == config.iOS_MAX:
            return True
        if device_type == 'android' and version == config.ANDROID_MAX:
            return True
        return False

    def _get_market_info(self, request, device_type):
        market = request.market.upper()
        dl_key = '{}_DL'.format(market)
        if dl_key not in settings.CONSTANCE_CONFIG:
            if device_type == 'ios':
                return dict(
                    url=config.iOS_SIBAPP_DL,
                    max=config.iOS_MAX,
                    min=config.iOS_MIN,
                    update_log=config.iOS_UPDATE_LOG
                )
            else:
                return dict(
                    url=config.ANDROID_DL,
                    max=config.ANDROID_MAX,
                    min=config.ANDROID_MIN,
                    update_log=config.ANDROID_UPDATE_LOG
                )

        max_key = '{}_MAX'.format(market)
        min_key = '{}_MIN'.format(market)
        update_log_key = '{}_UPDATE_LOG'.format(market)

        return dict(
            url=config.__getattr__(dl_key),
            max=config.__getattr__(max_key),
            min=config.__getattr__(min_key),
            update_log=config.__getattr__(update_log_key)
        )

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

        udid = data.get('udid', 'not-set')
        one_signal_id = data.get('one_signal_id')
        bundle = get_not_none(data, 'bundle', 'com.application.canto')
        market_config = self._get_market_info(request, device_type)

        res = dict(
            force_update=False,
            suggest_update=False,
            is_token_valid=False,
            url=market_config['url'],
            token=''
        )

        if not request.user.is_anonymous:
            res['is_token_valid'] = True
            Device.objects.update_or_create(udid=udid,
                                            bundle=bundle,
                                            user=request.user,
                                            defaults={
                                                'one_signal_id': one_signal_id,
                                                'build_version': build_version,
                                                'type': device_type,
                                                'market': request.market
                                            }
                                            )
        else:
            if self._is_last_version(device_type, build_version) and random.random() < 0.0:
                user = User.create_guest_user()
                token = Token.generate_guest_token(user=user)
                res['token'] = token.key
                res['is_token_valid'] = True
                Device.objects.create(udid=udid,
                                      user=user,
                                      bundle=bundle,
                                      one_signal_id=one_signal_id,
                                      build_version=build_version,
                                      type=device_type,
                                      market=request.market
                                      )
            else:
                res['is_token_valid'] = False
                Device.objects.create(udid=udid,
                                      bundle=bundle,
                                      one_signal_id=one_signal_id,
                                      build_version=build_version,
                                      type=device_type,
                                      market=request.market
                                      )

        if build_version < market_config['min']:
            res['force_update'] = True
        elif build_version < market_config['max']:
            res['suggest_update'] = True

        if res['force_update'] or res['suggest_update']:
            res['update_log'] = market_config['update_log']

        return Response(data=res)
