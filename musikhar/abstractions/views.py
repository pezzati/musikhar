import ast

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import mixins, GenericViewSet

from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.middlewares import error_logger
from musikhar.utils import conn, convert_to_dict


class IgnoreCsrfAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class PermissionModelViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):
    search_class = None

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

    def do_pagination(self, queryset, serializer_class=None, cache_key='', cache_time=900):
        if serializer_class is None:
            serializer_class = self.serializer_class
        try:
            page = self.paginate_queryset(queryset)
        except NotFound:
            page = None
        if page is not None:
            serializer = serializer_class(page, many=True, context={'request': self.request, 'caller': serializer_class.Meta.model})
            response = self.get_paginated_response(serializer.data)
            if cache_key:
                conn().set(name=cache_key, value=dict(response.data), ex=cache_time)
            return response
        serializer = serializer_class(queryset, many=True, context={'request': self.request, 'caller': serializer_class.Meta.model})
        if cache_key:
            conn().set(name=cache_key, value=serializer.data, ex=cache_time)
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
            return self.do_pagination(queryset=search.get_result(search_key=key, tags=tags))
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))


class PermissionReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                                     mixins.ListModelMixin,
                                     GenericViewSet):
    search_class = None

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

    def do_pagination(self, queryset, serializer_class=None, cache_key='', cache_time=900):
        if serializer_class is None:
            serializer_class = self.serializer_class
        try:
            page = self.paginate_queryset(queryset)
        except NotFound:
            page = None
        if page is not None:
            serializer = serializer_class(page, many=True, context={'request': self.request, 'caller': serializer_class.Meta.model})
            response = self.get_paginated_response(serializer.data)
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
            return self.do_pagination(queryset=search.get_result(search_key=key, tags=tags))
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

    @staticmethod
    def cache_response(request):
        raw_data = conn().get(request.get_full_path())
        if raw_data:
            try:
                return Response(ast.literal_eval(raw_data.decode('utf-8')))
            except Exception as e:
                error_logger.info('[CACHE_RESPONSE] ERROR: {}, raw_data: {}'.format(str(e), raw_data))
        return None
