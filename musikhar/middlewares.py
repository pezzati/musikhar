from django.utils.deprecation import MiddlewareMixin


class DomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.domain = request.META['HTTP_HOST']
