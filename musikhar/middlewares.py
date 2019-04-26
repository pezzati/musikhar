import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin
from constance import config

from musikhar.utils import PLATFORM_IOS


class DomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.device_type = request.META.get('HTTP_DEVICETYPE', 'android').lower()
        request.market = request.META.get('HTTP_MARKET', 'default').lower()

        request.domain = request.META['HTTP_HOST']


error_logger = logging.getLogger("error")
stg_logger = logging.getLogger("staging")


class CatchTheException(MiddlewareMixin):
    def process_exception(self, request, exception):
        import traceback
        error_logger.info('[{}] EXCEPTION : {} \n \t tracback: \n {}'.format(datetime.now(),
                                                                             str(exception).encode('utf-8'),
                                                                             traceback.format_exc()
                                                                             )
                          )


class StagingLogger(MiddlewareMixin):
    def process_request(self, request):
        log = '{} -- {} -- {} -- {}'.format(datetime.now(),
                                            request.META['PATH_INFO'],
                                            request.META['CONTENT_LENGTH'],
                                            request.body)
        stg_logger.info(log)


class VersionMiddleWare(MiddlewareMixin):

    def process_response(self, request, response):
        if request.device_type == PLATFORM_IOS:
            response['MAX_BUILD_VERSION'] = config.iOS_MAX
            response['MIN_BUILD_VERSION'] = config.iOS_MIN
        else:
            response['MAX_BUILD_VERSION'] = config.ANDROID_MAX
            response['MIN_BUILD_VERSION'] = config.ANDROID_MIN
        return response
