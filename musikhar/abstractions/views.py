from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
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
