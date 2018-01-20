from rest_framework import status
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
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serial_number = request.data.get('serial_number')
        if not serial_number:
            # TODO response msg
            return Response(status=status.HTTP_400_BAD_REQUEST)

        package = BusinessPackage.get_package(code=serial_number)
        if not package:
            # TODO response msg
            return Response(status=status.HTTP_404_NOT_FOUND)

        package.apply_package(user=request.user)
        return Response()



