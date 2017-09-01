from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from loginapp.auth import CsrfExemptSessionAuthentication


class IgnoreCsrfAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class PermissionReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
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

    def do_pagination(self, queryset, serializer_class=None):
        if serializer_class is None:
            serializer_class = self.serializer_class
        try:
            page = self.paginate_queryset(queryset)
        except NotFound:
            page = None
        if page is not None:
            serializer = serializer_class(page, many=True, context={'request': self.request, 'caller': serializer_class.Meta.model})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True, context={'request': self.request, 'caller': serializer_class.Meta.model})
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(PermissionReadOnlyModelViewSet, self).get_serializer_context()
        context['caller'] = self.serializer_class.Meta.model
        return context
