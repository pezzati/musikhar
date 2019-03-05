import ast

from rest_framework import status, exceptions
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import mixins, GenericViewSet

from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.middlewares import error_logger
from musikhar.utils import conn, convert_to_dict, PLATFORM_ANDROID


class IgnoreCsrfAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            elif isinstance(exc, exceptions.NotAuthenticated):
                exc.status_code = status.HTTP_401_UNAUTHORIZED
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        return response


class PermissionModelViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):
    search_class = None
    list_cache = False

    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            elif isinstance(exc, exceptions.NotAuthenticated):
                exc.status_code = status.HTTP_401_UNAUTHORIZED
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 403:
            # TODO fix this shit :))
            response.data = dict(
                error='forbiden'
            )
        return super(PermissionModelViewSet, self).finalize_response(request=request,
                                                                     response=response,
                                                                     args=args,
                                                                     kwargs=kwargs)

    def options(self, request, *args, **kwargs):
        raise PermissionDenied

    def create(self, request, *args, **kwargs):
        try:
            return super(PermissionModelViewSet, self).create(request, args, kwargs)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'msg': str(e)})

    def get_paginated_response(self, data, desc=''):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, desc=desc)

    def do_pagination(self, queryset, serializer_class=None, cache_key='', cache_time=900, desc=''):
        if serializer_class is None:
            serializer_class = self.serializer_class
        context = self.get_serializer_context()
        context['request'] = self.request
        context['caller'] = serializer_class.Meta.model
        try:
            page = self.paginate_queryset(queryset)
        except NotFound:
            page = None
        if page is not None:
            serializer = serializer_class(page, many=True, context=context)
            response = self.get_paginated_response(serializer.data, desc=desc)
            if cache_key:
                conn().set(name=cache_key, value=convert_to_dict(response.data), ex=cache_time)
            return response
        serializer = serializer_class(queryset, many=True, context=context)
        if cache_key:
            conn().set(name=cache_key, value=convert_to_dict(serializer.data), ex=cache_time)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(PermissionModelViewSet, self).get_serializer_context()
        context['caller'] = self.serializer_class.Meta.model
        return context

    @list_route()
    def search(self, request):
        if not self.search_class:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED, data='search_class not defined')
        search = self.search_class()
        key = request.GET.get('key')
        tags = request.GET.getlist('tags[]')
        try:
            return self.do_pagination(queryset=search.get_result(search_key=key, tags=tags, query_set=self.get_queryset()))
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

    @staticmethod
    def cache_response(request):
        if request.device_type == PLATFORM_ANDROID and request.market == 'default':
            raw_data = conn().get(request.get_full_path()+'#'+PLATFORM_ANDROID)
        else:
            raw_data = conn().get(request.get_full_path())
        if raw_data:
            try:
                return Response(ast.literal_eval(raw_data.decode('utf-8')))
            except Exception as e:
                error_logger.info('[CACHE_RESPONSE] ERROR: {}, request: {}, raw_data: {}'.format(str(e),
                                                                                                 request.get_full_path(),
                                                                                                 raw_data))
        return None


class PermissionReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                                     mixins.ListModelMixin,
                                     GenericViewSet):
    search_class = None
    list_cache = False

    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            elif isinstance(exc, exceptions.NotAuthenticated):
                exc.status_code = status.HTTP_401_UNAUTHORIZED
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        return response

    def list(self, request, *args, **kwargs):
        if self.list_cache:
            cached_response = self.cache_response(request=request)
            if cached_response:
                return cached_response

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            if self.list_cache:
                conn().set(name=request.get_full_path(), value=convert_to_dict(response.data), ex=86400)
                return response
            return response

        serializer = self.get_serializer(queryset, many=True)
        if self.list_cache:
            conn().set(name=request.get_full_path(), value=convert_to_dict(serializer.data), ex=86400)
        return Response(serializer.data)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 403:
            # TODO fix this shit :))
            response.data = dict(
                error='forbiden'
            )
        return super(PermissionReadOnlyModelViewSet, self).finalize_response(request=request,
                                                                             response=response,
                                                                             args=args,
                                                                             kwargs=kwargs)

    def options(self, request, *args, **kwargs):
        raise PermissionDenied

    def get_paginated_response(self, data, desc=''):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, desc=desc)

    def do_pagination(self, queryset, serializer_class=None, cache_key='', cache_time=900, desc=''):
        if serializer_class is None:
            serializer_class = self.serializer_class
        try:
            page = self.paginate_queryset(queryset)
        except NotFound:
            page = None
        if page is not None:
            serializer = serializer_class(page, many=True, context={'request': self.request, 'caller': serializer_class.Meta.model})
            response = self.get_paginated_response(serializer.data, desc=desc)
            if cache_key:
                conn().set(name=cache_key, value=convert_to_dict(response.data), ex=cache_time)
            return response
        serializer = serializer_class(queryset, many=True, context={'request': self.request, 'caller': serializer_class.Meta.model})
        if cache_key:
            conn().set(name=cache_key, value=convert_to_dict(serializer.data), ex=cache_time)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(PermissionReadOnlyModelViewSet, self).get_serializer_context()
        context['caller'] = self.serializer_class.Meta.model
        return context

    @list_route()
    def search(self, request):
        if not self.search_class:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED, data='search_class not defined')
        search = self.search_class()
        key = request.GET.get('key')
        tags = request.GET.get('tags[]')
        try:
            return self.do_pagination(queryset=search.get_result(search_key=key, tags=tags, query_set=self.get_queryset()))
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

    @staticmethod
    def cache_response(request):
        if request.device_type == PLATFORM_ANDROID and request.market == 'default':
            raw_data = conn().get(request.get_full_path()+'#'+PLATFORM_ANDROID)
        else:
            raw_data = conn().get(request.get_full_path())
        if raw_data:
            try:
                return Response(ast.literal_eval(raw_data.decode('utf-8')))
            except Exception as e:
                error_logger.info('[CACHE_RESPONSE] ERROR: {}, request: {}, raw_data: {}'.format(str(e),
                                                                                                 request.get_full_path(),
                                                                                                 raw_data))
        return None
