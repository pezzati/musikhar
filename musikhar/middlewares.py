import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin


class DomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
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
