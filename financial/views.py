from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from financial.models import BusinessPackage
from financial.serializers import BusinessPackageSerializer
from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet, IgnoreCsrfAPIView


class BusinessPackagesViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = BusinessPackageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = BusinessPackage.objects.filter(active=True)
    list_cache = False


class Purchase(IgnoreCsrfAPIView):
    def post(self, request):
        return Response()



